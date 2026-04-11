"""
Event Logger Service — Evaluation Data Collection

Logs all platform events for experiment analysis:
- Submissions, recommendations shown/clicked, page views, hint requests
- Each event includes timestamp, student_id, session_id, and event-specific data
"""

import logging
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tables import (
    EventLog,
    ExperimentGroup,
    KnowledgeState,
    EloRating,
    FsrsCard,
)

logger = logging.getLogger(__name__)


async def log_event(
    session: AsyncSession,
    user_id: str,
    event: str,
    data: dict | None = None,
    session_id: str | None = None,
) -> dict:
    """Log a single event."""
    log = EventLog(
        user_id=user_id,
        event=event,
        data=data or {},
        session_id=session_id,
    )
    session.add(log)
    await session.commit()
    return {"id": log.id, "event": event, "timestamp": str(log.created_at)}


async def get_user_group(session: AsyncSession, user_id: str) -> str | None:
    """Get experiment group for a user."""
    result = await session.execute(
        select(ExperimentGroup.group_name).where(
            ExperimentGroup.user_id == user_id
        )
    )
    return result.scalar_one_or_none()


async def assign_group(
    session: AsyncSession, user_id: str, group_name: str
) -> dict:
    """Assign a user to an experiment group."""
    existing = await session.execute(
        select(ExperimentGroup).where(ExperimentGroup.user_id == user_id)
    )
    group = existing.scalar_one_or_none()
    if group:
        group.group_name = group_name
    else:
        group = ExperimentGroup(user_id=user_id, group_name=group_name)
        session.add(group)
    await session.commit()
    return {"user_id": user_id, "group": group_name}


async def export_events(
    session: AsyncSession,
    event_type: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    limit: int = 10000,
) -> list[dict]:
    """Export event logs for analysis."""
    query = select(EventLog).order_by(EventLog.created_at)

    if event_type:
        query = query.where(EventLog.event == event_type)
    if start_date:
        query = query.where(EventLog.created_at >= start_date)
    if end_date:
        query = query.where(EventLog.created_at <= end_date)

    query = query.limit(limit)
    result = await session.execute(query)
    logs = result.scalars().all()

    return [
        {
            "id": log.id,
            "user_id": str(log.user_id),
            "event": log.event,
            "data": log.data,
            "session_id": log.session_id,
            "created_at": log.created_at.isoformat() + "Z" if log.created_at else None,
        }
        for log in logs
    ]


async def export_knowledge_snapshots(session: AsyncSession) -> list[dict]:
    """Export current BKT knowledge states for all students."""
    result = await session.execute(
        select(KnowledgeState).order_by(
            KnowledgeState.student_id, KnowledgeState.concept_id
        )
    )
    states = result.scalars().all()
    return [
        {
            "student_id": str(s.student_id),
            "concept_id": s.concept_id,
            "p_mastery": round(s.p_mastery, 4),
            "n_attempts": s.n_attempts,
            "n_correct": s.n_correct,
            "updated_at": s.updated_at.isoformat() + "Z" if s.updated_at else None,
        }
        for s in states
    ]


async def export_elo_ratings(session: AsyncSession) -> list[dict]:
    """Export all Elo ratings for analysis."""
    result = await session.execute(
        select(EloRating).order_by(EloRating.entity_type, EloRating.entity_id)
    )
    ratings = result.scalars().all()
    return [
        {
            "entity_id": str(r.entity_id),
            "entity_type": r.entity_type,
            "concept_id": r.concept_id,
            "rating": round(r.rating, 2),
            "k_value": round(r.k_value, 2),
            "trend": round(r.trend, 4),
            "n_attempts": r.n_attempts,
            "rating_history": r.rating_history,
        }
        for r in ratings
    ]


async def export_fsrs_cards(session: AsyncSession) -> list[dict]:
    """Export all FSRS card states for analysis."""
    result = await session.execute(
        select(FsrsCard).order_by(FsrsCard.student_id, FsrsCard.concept_id)
    )
    cards = result.scalars().all()
    return [
        {
            "student_id": str(c.student_id),
            "concept_id": c.concept_id,
            "difficulty": round(c.difficulty, 4),
            "stability": round(c.stability, 4),
            "retrievability": round(c.retrievability, 4),
            "state": c.state,
            "due_date": c.due_date.isoformat() + "Z" if c.due_date else None,
            "reps": c.reps,
            "lapses": c.lapses,
        }
        for c in cards
    ]


async def get_experiment_stats(session: AsyncSession) -> dict:
    """Get summary statistics for the experiment."""
    # Count by group
    group_counts = await session.execute(
        select(
            ExperimentGroup.group_name,
            func.count(ExperimentGroup.id),
        ).group_by(ExperimentGroup.group_name)
    )
    groups = {row[0]: row[1] for row in group_counts.all()}

    # Count events by type
    event_counts = await session.execute(
        select(
            EventLog.event,
            func.count(EventLog.id),
        ).group_by(EventLog.event)
    )
    events = {row[0]: row[1] for row in event_counts.all()}

    # Total unique users with events
    user_count = await session.execute(
        select(func.count(func.distinct(EventLog.user_id)))
    )
    total_users = user_count.scalar() or 0

    return {
        "experiment_groups": groups,
        "event_counts": events,
        "total_active_users": total_users,
    }
