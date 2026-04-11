"""
Adaptive Engine — Pipeline Orchestrator

Coordinates all 4 adaptive layers (BKT, Elo, MAB, FSRS) for:
1. Processing submission results (update all layers)
2. Generating recommendations (query all layers)
3. Providing complete knowledge state for dashboard

Feature flags (from config/env) control which layers are active:
- ENABLE_BKT, ENABLE_ELO, ENABLE_MAB, ENABLE_FSRS
This enables control-group mode for evaluation (disable all = content-based only).
"""

import asyncio
import logging

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import async_session
from app.models.tables import (
    Concept,
    EloRating,
    KnowledgeGraphEdge,
    KnowledgeState,
    Problem,
    ProblemConcept,
    Submission,
)
from app.services.bkt_service import BKTService
from app.services.cache_service import cache
from app.services.elo_service import EloService
from app.services.fsrs_service import FSRSService, submission_to_fsrs_rating
from app.services.mab_service import MABService, compute_reward

logger = logging.getLogger(__name__)


class AdaptiveEngine:
    """Orchestrates all adaptive layers."""

    def __init__(self):
        self.bkt = BKTService()
        self.elo = EloService()
        self.mab = MABService()
        self.fsrs = FSRSService()

    async def process_submission(
        self,
        session: AsyncSession,
        student_id: str,
        problem_id: str,
        is_correct: bool,
        attempt_number: int = 1,
        time_spent_seconds: float = 0,
    ) -> dict:
        """
        Update all adaptive layers after a submission.
        Called asynchronously after code execution completes.
        """
        # Get primary concept for this problem
        pc_result = await session.execute(
            select(ProblemConcept).where(
                ProblemConcept.problem_id == problem_id,
                ProblemConcept.is_primary == True,  # noqa: E712
            )
        )
        primary_mapping = pc_result.scalar_one_or_none()
        concept_id = primary_mapping.concept_id if primary_mapping else None

        # Get problem difficulty for Elo initialization
        prob_result = await session.execute(
            select(Problem.difficulty).where(Problem.id == problem_id)
        )
        raw_diff = prob_result.scalar_one_or_none()
        problem_difficulty = raw_diff.value if hasattr(raw_diff, 'value') else str(raw_diff or "MEDIUM")

        # --- Phase 1: BKT first (MAB reward depends on mastery delta) ---
        bkt_result = {}
        p_mastery_before = 0.1
        p_mastery_after = 0.1
        if settings.enable_bkt:
            bkt_result = await self.bkt.update(session, student_id, problem_id, is_correct)
            for update in bkt_result.get("updates", []):
                if update.get("is_primary"):
                    p_mastery_before = update["p_mastery_before"]
                    p_mastery_after = update["p_mastery_after"]
                    break

        # --- Phase 2: Elo, MAB, FSRS in parallel (each with its own session) ---
        async def update_elo():
            if not settings.enable_elo:
                return {}
            async with async_session() as s:
                result = await self.elo.update(
                    s, student_id, problem_id, is_correct, str(problem_difficulty)
                )
                return result

        async def update_mab():
            if not settings.enable_mab or concept_id is None:
                return {}
            reward = compute_reward(
                p_mastery_before,
                p_mastery_after,
                is_correct,
                attempt_number,
                time_spent_seconds,
            )
            async with async_session() as s:
                result = await self.mab.update(
                    s, student_id, concept_id, problem_id, reward
                )
                return result

        async def update_fsrs():
            if not settings.enable_fsrs or concept_id is None:
                return {}
            rating = submission_to_fsrs_rating(is_correct, attempt_number, time_spent_seconds)
            async with async_session() as s:
                result = await self.fsrs.review(s, student_id, concept_id, rating)
                return result

        elo_result, mab_result, fsrs_result = await asyncio.gather(
            update_elo(), update_mab(), update_fsrs()
        )

        # Invalidate cached data for this student
        await cache.invalidate_student(student_id)

        return {
            "bkt_update": bkt_result,
            "elo_update": elo_result,
            "mab_update": mab_result,
            "fsrs_update": fsrs_result,
        }

    async def get_recommendations(
        self,
        session: AsyncSession,
        student_id: str,
        limit: int = 5,
    ) -> dict:
        """Get adaptive recommendations using all layers."""
        # Check cache first
        cached = await cache.get_recommendations(student_id)
        if cached:
            return cached

        # Get MAB recommendations
        mab_result = await self.mab.recommend(session, student_id, limit)

        # Build concept display name lookup
        concepts_result = await session.execute(select(Concept))
        concept_lookup = {c.id: c for c in concepts_result.scalars().all()}

        # Enrich with Elo data and frontend-expected fields
        student_elo_data = await self.elo.get_student_elo(session, student_id)

        for rec in mab_result.get("recommendations", []):
            problem_elo_data = await self.elo.get_problem_elo(session, rec["problem_id"])
            student_rating = student_elo_data["rating"]
            problem_rating = problem_elo_data["rating"]

            rec["difficulty_match"] = round(
                1.0 - abs(problem_rating - student_rating - 200) / 400, 4
            )
            rec["expected_success"] = round(
                1.0 / (1.0 + 10 ** ((problem_rating - student_rating) / 400)), 4
            )
            rec["problem_elo"] = problem_rating

            # Add fields expected by frontend
            rec["title"] = rec.get("problem_title", "")

            # Get problem difficulty from DB
            prob_result = await session.execute(
                select(Problem.difficulty).where(Problem.id == rec["problem_id"])
            )
            difficulty_val = prob_result.scalar_one_or_none()
            rec["difficulty"] = difficulty_val.value if hasattr(difficulty_val, "value") else str(difficulty_val or "MEDIUM")

            # Add concept display name
            concept = concept_lookup.get(rec.get("concept_id"))
            rec["concept_display_name"] = concept.display_name if concept else rec.get("concept_name", "")

            # Score based on difficulty match
            rec["score"] = rec["difficulty_match"]

        # Add knowledge summary
        knowledge_states = await self.bkt.get_state(session, student_id)
        review_queue = await self.fsrs.get_review_queue(session, student_id)

        mastered = sum(1 for s in knowledge_states if s["status"] == "MASTERED")
        in_progress = sum(1 for s in knowledge_states if s["status"] == "IN_PROGRESS")

        # Count locked concepts
        concepts_result = await session.execute(select(func.count(Concept.id)))
        total_concepts = concepts_result.scalar() or 0
        locked = total_concepts - mastered - in_progress - sum(
            1 for s in knowledge_states if s["status"] == "NOT_STARTED"
        )
        locked = max(0, total_concepts - len(knowledge_states))

        mab_result["knowledge_summary"] = {
            "mastered_concepts": mastered,
            "in_progress_concepts": in_progress,
            "locked_concepts": locked,
            "total_concepts": total_concepts,
            "student_elo": student_elo_data["rating"],
            "elo_trend": (
                "IMPROVING" if student_elo_data["trend"] > 0.05
                else "DECLINING" if student_elo_data["trend"] < -0.05
                else "STABLE"
            ),
            "due_reviews": len(review_queue["due_now"]),
        }

        await cache.set_recommendations(student_id, mab_result)
        return mab_result

    async def get_knowledge_state(
        self, session: AsyncSession, student_id: str
    ) -> dict:
        """Complete knowledge state for dashboard visualization."""
        # Check cache first
        cached = await cache.get_knowledge_state(student_id)
        if cached:
            return cached

        knowledge_states = await self.bkt.get_state(session, student_id)
        student_elo = await self.elo.get_student_elo(session, student_id)
        review_queue = await self.fsrs.get_review_queue(session, student_id)

        # Get knowledge graph
        concepts_result = await session.execute(
            select(Concept).order_by(Concept.difficulty_tier)
        )
        concepts = concepts_result.scalars().all()

        edges_result = await session.execute(select(KnowledgeGraphEdge))
        edges = edges_result.scalars().all()

        # Build prerequisite map
        prereq_map: dict[int, list[int]] = {}
        for edge in edges:
            prereq_map.setdefault(edge.to_concept_id, []).append(edge.from_concept_id)

        # Build knowledge states map
        ks_map = {s["concept_id"]: s for s in knowledge_states}
        due_map = {d["concept_id"]: d for d in review_queue["due_now"]}

        # Determine status for each concept
        # Status mapping: frontend expects lowercase 'mastered' | 'learning' | 'not_started'
        concept_data = []
        concept_status_map = {}  # id -> status for graph nodes
        concept_mastery_map = {}  # id -> p_mastery for graph nodes
        for concept in concepts:
            ks = ks_map.get(concept.id, {})
            mastery = ks.get("p_mastery", 0.0)

            # Check prerequisites
            prereqs = prereq_map.get(concept.id, [])
            prereqs_met = all(
                ks_map.get(p_id, {}).get("p_mastery", 0) >= 0.85
                for p_id in prereqs
            )

            if mastery >= 0.85:
                status = "mastered"
            elif mastery > 0.1 or ks.get("n_attempts", 0) > 0:
                status = "learning"
            else:
                status = "not_started"

            concept_status_map[concept.id] = status
            concept_mastery_map[concept.id] = round(mastery, 4)

            due_info = due_map.get(concept.id)

            concept_data.append({
                "concept_id": concept.id,
                "concept_name": concept.name,
                "display_name": concept.display_name,
                "topic_group": concept.topic_group,
                "difficulty_tier": concept.difficulty_tier,
                "p_mastery": round(mastery, 4),
                "status": status,
                "prerequisites_met": prereqs_met,
                "n_attempts": ks.get("n_attempts", 0),
                "n_correct": ks.get("n_correct", 0),
                "fsrs_due": due_info is not None,
                "retrievability": due_info["retrievability"] if due_info else None,
            })

        # Compute summary
        total_concepts = len(concept_data)
        mastered_count = sum(1 for c in concept_data if c["status"] == "mastered")
        learning_count = sum(1 for c in concept_data if c["status"] == "learning")
        not_started_count = sum(1 for c in concept_data if c["status"] == "not_started")
        overall_mastery = (
            sum(c["p_mastery"] for c in concept_data) / total_concepts
            if total_concepts > 0 else 0.0
        )

        result = {
            "concepts": concept_data,
            "student_elo": student_elo,
            "review_queue": review_queue,
            "knowledge_graph": {
                "nodes": [
                    {
                        "id": c.id,
                        "name": c.name,
                        "display_name": c.display_name,
                        "topic_group": c.topic_group,
                        "difficulty_tier": c.difficulty_tier,
                        "p_mastery": concept_mastery_map.get(c.id, 0.0),
                        "status": concept_status_map.get(c.id, "not_started"),
                    }
                    for c in concepts
                ],
                "edges": [
                    {
                        "from_id": e.from_concept_id,
                        "to_id": e.to_concept_id,
                    }
                    for e in edges
                ],
            },
            "summary": {
                "total_concepts": total_concepts,
                "mastered": mastered_count,
                "learning": learning_count,
                "not_started": not_started_count,
                "overall_mastery": round(overall_mastery, 4),
            },
        }
        await cache.set_knowledge_state(student_id, result)
        return result
