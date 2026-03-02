"""
Evaluation & Experiment endpoints.

Data collection, export, and experiment management for thesis evaluation.
"""

from datetime import datetime

from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, verify_service_key
from app.services.event_logger import (
    log_event,
    assign_group,
    get_user_group,
    export_events,
    export_knowledge_snapshots,
    export_elo_ratings,
    export_fsrs_cards,
    get_experiment_stats,
)

router = APIRouter(
    prefix="/evaluation",
    tags=["evaluation"],
    dependencies=[Depends(verify_service_key)],
)


# --- Event Logging ---


class LogEventRequest(BaseModel):
    user_id: str
    event: str = Field(..., max_length=50)
    data: dict = Field(default_factory=dict)
    session_id: str | None = None


@router.post("/log")
async def log(
    request: LogEventRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """Log a platform event for evaluation."""
    return await log_event(
        session=session,
        user_id=request.user_id,
        event=request.event,
        data=request.data,
        session_id=request.session_id,
    )


# --- Experiment Group Management ---


class AssignGroupRequest(BaseModel):
    user_id: str
    group: str = Field(..., pattern="^(experimental|control)$")


@router.post("/assign-group")
async def assign(
    request: AssignGroupRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """Assign a user to experimental or control group."""
    return await assign_group(session, request.user_id, request.group)


@router.get("/group/{user_id}")
async def get_group(
    user_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    """Get a user's experiment group."""
    group = await get_user_group(session, user_id)
    return {"user_id": user_id, "group": group}


# --- Data Export ---


@router.get("/export/events")
async def export_event_logs(
    event_type: str | None = Query(None),
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    limit: int = Query(10000, ge=1, le=100000),
    session: AsyncSession = Depends(get_db_session),
):
    """Export event logs (JSON). Filter by event type and date range."""
    events = await export_events(session, event_type, start_date, end_date, limit)
    return {"count": len(events), "events": events}


@router.get("/export/knowledge-states")
async def export_knowledge(
    session: AsyncSession = Depends(get_db_session),
):
    """Export all BKT knowledge state snapshots."""
    states = await export_knowledge_snapshots(session)
    return {"count": len(states), "knowledge_states": states}


@router.get("/export/elo-ratings")
async def export_elo(
    session: AsyncSession = Depends(get_db_session),
):
    """Export all Elo ratings (students + problems)."""
    ratings = await export_elo_ratings(session)
    return {"count": len(ratings), "elo_ratings": ratings}


@router.get("/export/fsrs-cards")
async def export_fsrs(
    session: AsyncSession = Depends(get_db_session),
):
    """Export all FSRS card states."""
    cards = await export_fsrs_cards(session)
    return {"count": len(cards), "fsrs_cards": cards}


# --- Experiment Statistics ---


@router.get("/stats")
async def stats(
    session: AsyncSession = Depends(get_db_session),
):
    """Get experiment summary statistics."""
    return await get_experiment_stats(session)
