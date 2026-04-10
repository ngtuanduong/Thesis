"""
Layer 3: Hierarchical Multi-Armed Bandit (MAB) Service

Implements Thompson Sampling with Beta priors for 2-level selection:
Level 1: Concept selection (which topic to study)
Level 2: Problem selection (which specific problem within the concept)
"""

import logging
from datetime import datetime, timedelta, timezone

import numpy as np
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tables import (
    Concept,
    FsrsCard,
    KnowledgeGraphEdge,
    KnowledgeState,
    MabState,
    ProblemConcept,
    Problem,
    Submission,
)
from app.config import settings
from app.services.elo_service import EloService

logger = logging.getLogger(__name__)

elo_service = EloService()


def thompson_select(arms: list[dict]) -> dict | None:
    """Select arm with highest sampled value from Beta distribution."""
    if not arms:
        return None

    best_arm = None
    best_sample = -1.0

    for arm in arms:
        sample = np.random.beta(arm["alpha"], arm["beta"])
        if sample > best_sample:
            best_sample = sample
            best_arm = arm

    return best_arm


def compute_reward(
    p_mastery_before: float,
    p_mastery_after: float,
    is_correct: bool,
    attempt_number: int,
    time_spent: float,
) -> float:
    """
    Compute MAB reward combining learning gain, difficulty match, and efficiency.
    """
    # Component 1: Learning gain (weight: 0.5)
    learning_gain = p_mastery_after - p_mastery_before

    # Component 2: Difficulty match (weight: 0.3)
    if is_correct and attempt_number <= 3:
        difficulty_reward = 1.0
    elif is_correct and attempt_number > 3:
        difficulty_reward = 0.5
    elif not is_correct and attempt_number >= 3:
        difficulty_reward = 0.0
    else:
        difficulty_reward = 0.3

    # Component 3: Efficiency (weight: 0.2)
    efficiency = min(1.0, 300.0 / max(time_spent, 30.0))

    # Weighted combination with gain scaling
    reward = (
        0.5 * max(0, learning_gain * 10)
        + 0.3 * difficulty_reward
        + 0.2 * efficiency
    )

    return min(1.0, max(0.0, reward))


class MABService:
    """Service for Hierarchical Multi-Armed Bandit operations."""

    async def _get_or_create_arm(
        self,
        session: AsyncSession,
        student_id: str,
        arm_id: str,
        arm_type: str,
    ) -> MabState:
        """Get or create MAB arm state."""
        result = await session.execute(
            select(MabState).where(
                MabState.student_id == student_id,
                MabState.arm_id == arm_id,
                MabState.arm_type == arm_type,
            )
        )
        state = result.scalar_one_or_none()

        if state is None:
            state = MabState(
                student_id=student_id,
                arm_id=arm_id,
                arm_type=arm_type,
                alpha=1.0,
                beta=1.0,
                n_pulls=0,
                total_reward=0.0,
            )
            session.add(state)
            await session.flush()

        return state

    async def _get_eligible_concepts(
        self, session: AsyncSession, student_id: str
    ) -> list[dict]:
        """Get concepts eligible for recommendation (prerequisites met, not fully mastered)."""
        # Get all concepts
        concepts_result = await session.execute(
            select(Concept).order_by(Concept.difficulty_tier)
        )
        all_concepts = concepts_result.scalars().all()

        # Get knowledge states
        ks_result = await session.execute(
            select(KnowledgeState).where(KnowledgeState.student_id == student_id)
        )
        knowledge_states = {ks.concept_id: ks.p_mastery for ks in ks_result.scalars().all()}

        # Get prerequisite edges
        edges_result = await session.execute(select(KnowledgeGraphEdge))
        edges = edges_result.scalars().all()
        prereq_map: dict[int, list[int]] = {}
        for edge in edges:
            if edge.relation_type == "PREREQUISITE":
                prereq_map.setdefault(edge.to_concept_id, []).append(edge.from_concept_id)

        # Get due reviews for FSRS
        due_concept_ids = set()
        fsrs_result = await session.execute(
            select(FsrsCard).where(
                FsrsCard.student_id == student_id,
                FsrsCard.state != "NEW",
            )
        )
        now = datetime.utcnow()
        for card in fsrs_result.scalars().all():
            if card.last_review:
                elapsed = (now - card.last_review).total_seconds() / 86400
                r = (1 + elapsed / (9 * max(card.stability, 0.1))) ** (-1)
                if r < 0.9:
                    due_concept_ids.add(card.concept_id)

        eligible = []
        for concept in all_concepts:
            prereqs = prereq_map.get(concept.id, [])
            all_prereqs_met = all(
                knowledge_states.get(p_id, 0) >= settings.prereq_mastery_threshold
                for p_id in prereqs
            )

            mastery = knowledge_states.get(concept.id, 0.0)
            is_mastered = mastery >= settings.mastered_threshold
            is_due_review = concept.id in due_concept_ids

            if all_prereqs_met and (not is_mastered or is_due_review):
                eligible.append({
                    "concept_id": concept.id,
                    "concept_name": concept.name,
                    "display_name": concept.display_name,
                    "mastery": round(mastery, 4),
                    "is_due_review": is_due_review,
                })

        return eligible

    async def recommend(
        self,
        session: AsyncSession,
        student_id: str,
        n_recommendations: int = 5,
    ) -> dict:
        """Full hierarchical MAB recommendation pipeline."""
        recommendations = []
        eligible_concepts = await self._get_eligible_concepts(session, student_id)

        if not eligible_concepts:
            return {"recommendations": [], "message": "No eligible concepts found"}

        # Get knowledge states for status
        ks_result = await session.execute(
            select(KnowledgeState).where(KnowledgeState.student_id == student_id)
        )
        knowledge_states = {ks.concept_id: ks.p_mastery for ks in ks_result.scalars().all()}

        # Step 1: FSRS-MAB conflict resolution with threshold mechanism
        due_reviews = [c for c in eligible_concepts if c["is_due_review"]]

        # Separate critical vs standard reviews
        critical_reviews = []
        standard_reviews = []
        for review in due_reviews:
            # Approximate retrievability from mastery (simplified)
            r = review.get("retrievability", 0.8)
            if r < 0.7:
                critical_reviews.append(review)
            else:
                standard_reviews.append(review)

        n_critical = min(len(critical_reviews), n_recommendations)
        remaining = n_recommendations - n_critical
        n_standard = min(len(standard_reviews), remaining // 2)
        n_review = n_critical + n_standard
        n_new = n_recommendations - n_review

        if n_new == 0 and n_critical < n_recommendations:
            n_review -= 1
            n_new = 1

        # Step 2: Select review problems
        review_concepts = (critical_reviews + standard_reviews)[:n_review]
        for rc in review_concepts:
            problem = await self._select_problem_for_concept(
                session, student_id, rc["concept_id"]
            )
            if problem:
                recommendations.append({
                    "problem_id": problem["problem_id"],
                    "problem_title": problem["title"],
                    "concept_id": rc["concept_id"],
                    "concept_name": rc["concept_name"],
                    "reason": "REVIEW",
                    "mastery_before": rc["mastery"],
                })

        # Step 3: Level 1 MAB — Select new concepts
        new_concepts = [c for c in eligible_concepts if not c["is_due_review"]]
        selected_concept_ids = set()

        for _ in range(n_new):
            available = [c for c in new_concepts if c["concept_id"] not in selected_concept_ids]
            if not available:
                break

            # Get MAB arms for available concepts
            arms = []
            for c in available:
                arm_state = await self._get_or_create_arm(
                    session, student_id, str(c["concept_id"]), "CONCEPT"
                )
                arms.append({
                    "id": c["concept_id"],
                    "alpha": arm_state.alpha,
                    "beta": arm_state.beta,
                    "concept": c,
                })

            selected = thompson_select(arms)
            if not selected:
                break

            selected_concept_ids.add(selected["id"])

            # Step 4: Level 2 MAB — Select problem within concept
            problem = await self._select_problem_for_concept(
                session, student_id, selected["id"]
            )
            if problem:
                mastery = knowledge_states.get(selected["id"], 0.0)
                recommendations.append({
                    "problem_id": problem["problem_id"],
                    "problem_title": problem["title"],
                    "concept_id": selected["id"],
                    "concept_name": selected["concept"]["concept_name"],
                    "reason": "NEW_CONCEPT" if mastery < 0.5 else "PRACTICE",
                    "mastery_before": round(mastery, 4),
                })

        return {"recommendations": recommendations}

    async def _select_problem_for_concept(
        self,
        session: AsyncSession,
        student_id: str,
        concept_id: int,
    ) -> dict | None:
        """Level 2: Select specific problem within a concept using MAB + ZPD."""
        # Get problems for this concept
        result = await session.execute(
            select(ProblemConcept, Problem)
            .join(Problem, ProblemConcept.problem_id == Problem.id)
            .where(ProblemConcept.concept_id == concept_id)
        )
        problem_rows = result.all()

        if not problem_rows:
            return None

        # Filter out recently attempted (last 24h)
        cutoff = datetime.utcnow() - timedelta(hours=24)
        recent_result = await session.execute(
            select(Submission.problem_id)
            .where(
                Submission.user_id == student_id,
                Submission.created_at >= cutoff,
            )
            .distinct()
        )
        recent_problem_ids = {str(row[0]) for row in recent_result.all()}

        eligible = [
            (pc, p) for pc, p in problem_rows
            if str(p.id) not in recent_problem_ids
        ]

        # Fallback to all problems if none eligible
        if not eligible:
            eligible = list(problem_rows)

        if not eligible:
            return None

        # Thompson Sampling at problem level
        arms = []
        for pc, p in eligible:
            arm_state = await self._get_or_create_arm(
                session, student_id, str(p.id), "PROBLEM"
            )
            arms.append({
                "id": str(p.id),
                "alpha": arm_state.alpha,
                "beta": arm_state.beta,
                "title": p.title,
                "problem_id": str(p.id),
            })

        selected = thompson_select(arms)
        if not selected:
            return None

        return {"problem_id": selected["problem_id"], "title": selected["title"]}

    async def update(
        self,
        session: AsyncSession,
        student_id: str,
        concept_id: int,
        problem_id: str,
        reward: float,
    ) -> dict:
        """Update MAB state after observing a reward."""
        # Update concept-level arm
        concept_arm = await self._get_or_create_arm(
            session, student_id, str(concept_id), "CONCEPT"
        )
        concept_arm.alpha += reward
        concept_arm.beta += (1.0 - reward)
        concept_arm.n_pulls += 1
        concept_arm.total_reward += reward

        # Update problem-level arm
        problem_arm = await self._get_or_create_arm(
            session, student_id, problem_id, "PROBLEM"
        )
        problem_arm.alpha += reward
        problem_arm.beta += (1.0 - reward)
        problem_arm.n_pulls += 1
        problem_arm.total_reward += reward

        await session.commit()

        return {
            "concept_arm": {
                "alpha": round(concept_arm.alpha, 4),
                "beta": round(concept_arm.beta, 4),
                "n_pulls": concept_arm.n_pulls,
            },
            "problem_arm": {
                "alpha": round(problem_arm.alpha, 4),
                "beta": round(problem_arm.beta, 4),
                "n_pulls": problem_arm.n_pulls,
            },
            "reward": round(reward, 4),
        }

    async def get_state(
        self, session: AsyncSession, student_id: str
    ) -> dict:
        """Get MAB state for debugging/visualization."""
        result = await session.execute(
            select(MabState).where(
                MabState.student_id == student_id,
            ).order_by(MabState.arm_type, MabState.arm_id)
        )
        states = result.scalars().all()

        concept_arms = []
        problem_arms = []
        for s in states:
            arm_data = {
                "arm_id": s.arm_id,
                "alpha": round(s.alpha, 4),
                "beta": round(s.beta, 4),
                "n_pulls": s.n_pulls,
                "expected_reward": round(s.alpha / (s.alpha + s.beta), 4),
                "total_reward": round(s.total_reward, 4),
            }
            if s.arm_type == "CONCEPT":
                concept_arms.append(arm_data)
            else:
                problem_arms.append(arm_data)

        return {
            "student_id": student_id,
            "concept_arms": concept_arms,
            "problem_arms": problem_arms,
        }
