"""
Layer 1: Bayesian Knowledge Tracing (BKT) Service

Implements BKT update and predict functions for per-(student, concept) mastery estimation.
"""

import logging
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tables import Concept, KnowledgeState, ProblemConcept

logger = logging.getLogger(__name__)

# Default BKT parameters by concept difficulty tier
DEFAULT_PARAMS = {
    1: {"p_l0": 0.20, "p_transit": 0.30, "p_guess": 0.25, "p_slip": 0.10},  # Foundations
    2: {"p_l0": 0.15, "p_transit": 0.25, "p_guess": 0.20, "p_slip": 0.10},  # Core Skills
    3: {"p_l0": 0.10, "p_transit": 0.20, "p_guess": 0.15, "p_slip": 0.10},  # Intermediate
    4: {"p_l0": 0.07, "p_transit": 0.15, "p_guess": 0.12, "p_slip": 0.10},  # Advanced Application
    5: {"p_l0": 0.05, "p_transit": 0.10, "p_guess": 0.10, "p_slip": 0.10},  # Expert
}


@dataclass
class BKTParams:
    p_l0: float
    p_transit: float
    p_guess: float
    p_slip: float


def bkt_update(p_mastery: float, is_correct: bool, params: BKTParams) -> float:
    """
    Update mastery probability after a single observation.

    Args:
        p_mastery: Current P(L_t) before this observation
        is_correct: Whether the student answered correctly
        params: BKT parameters

    Returns:
        Updated P(L_{t+1}) after this observation
    """
    p_l = p_mastery
    p_g = params.p_guess
    p_s = params.p_slip

    if is_correct:
        p_correct = p_l * (1 - p_s) + (1 - p_l) * p_g
        p_l_given_obs = (p_l * (1 - p_s)) / p_correct if p_correct > 0 else p_l
    else:
        p_incorrect = p_l * p_s + (1 - p_l) * (1 - p_g)
        p_l_given_obs = (p_l * p_s) / p_incorrect if p_incorrect > 0 else p_l

    # Apply learning transition
    p_l_new = p_l_given_obs + (1 - p_l_given_obs) * params.p_transit

    # Clamp to valid range
    return max(0.001, min(0.999, p_l_new))


def predict_correctness(p_mastery: float, params: BKTParams) -> float:
    """Predict probability of correct response."""
    return p_mastery * (1 - params.p_slip) + (1 - p_mastery) * params.p_guess


class BKTService:
    """Service for Bayesian Knowledge Tracing operations."""

    async def get_or_create_state(
        self, session: AsyncSession, student_id: str, concept_id: int
    ) -> KnowledgeState:
        """Get existing knowledge state or create with defaults."""
        result = await session.execute(
            select(KnowledgeState).where(
                KnowledgeState.student_id == student_id,
                KnowledgeState.concept_id == concept_id,
            )
        )
        state = result.scalar_one_or_none()

        if state is None:
            # Get concept difficulty tier for default params
            concept_result = await session.execute(
                select(Concept).where(Concept.id == concept_id)
            )
            concept = concept_result.scalar_one_or_none()
            tier = concept.difficulty_tier if concept else 2
            defaults = DEFAULT_PARAMS.get(tier, DEFAULT_PARAMS[2])

            state = KnowledgeState(
                student_id=student_id,
                concept_id=concept_id,
                p_mastery=defaults["p_l0"],
                p_l0=defaults["p_l0"],
                p_transit=defaults["p_transit"],
                p_guess=defaults["p_guess"],
                p_slip=defaults["p_slip"],
                n_attempts=0,
                n_correct=0,
            )
            session.add(state)
            await session.flush()

        return state

    async def update(
        self,
        session: AsyncSession,
        student_id: str,
        problem_id: str,
        is_correct: bool,
    ) -> dict:
        """
        Update BKT after a submission. Handles multi-concept problems.

        Returns dict with update results for each concept.
        """
        # Get problem-concept mappings
        result = await session.execute(
            select(ProblemConcept).where(ProblemConcept.problem_id == problem_id)
        )
        mappings = result.scalars().all()

        if not mappings:
            logger.warning(f"No concept mapping for problem {problem_id}")
            return {"updates": []}

        updates = []
        for mapping in mappings:
            state = await self.get_or_create_state(
                session, student_id, mapping.concept_id
            )

            params = BKTParams(
                p_l0=state.p_l0,
                p_transit=state.p_transit,
                p_guess=state.p_guess,
                p_slip=state.p_slip,
            )

            p_before = state.p_mastery

            if mapping.is_primary:
                # Primary concept: full update
                state.p_mastery = bkt_update(state.p_mastery, is_correct, params)
                state.n_attempts += 1
                if is_correct:
                    state.n_correct += 1
            else:
                # Secondary concept: attenuated update (only on correct)
                if is_correct:
                    state.p_mastery = bkt_update(state.p_mastery, True, params)
                # Don't penalize secondary concepts on failure

            updates.append({
                "concept_id": mapping.concept_id,
                "is_primary": mapping.is_primary,
                "p_mastery_before": round(p_before, 4),
                "p_mastery_after": round(state.p_mastery, 4),
                "delta": round(state.p_mastery - p_before, 4),
            })

        await session.commit()
        return {"updates": updates}

    async def get_state(
        self, session: AsyncSession, student_id: str
    ) -> list[dict]:
        """Get all knowledge states for a student."""
        result = await session.execute(
            select(KnowledgeState, Concept)
            .join(Concept, KnowledgeState.concept_id == Concept.id)
            .where(KnowledgeState.student_id == student_id)
            .order_by(Concept.difficulty_tier, Concept.name)
        )
        rows = result.all()

        return [
            {
                "concept_id": ks.concept_id,
                "concept_name": c.name,
                "display_name": c.display_name,
                "p_mastery": round(ks.p_mastery, 4),
                "n_attempts": ks.n_attempts,
                "n_correct": ks.n_correct,
                "status": (
                    "MASTERED" if ks.p_mastery >= 0.85
                    else "IN_PROGRESS" if ks.p_mastery > 0.1
                    else "NOT_STARTED"
                ),
            }
            for ks, c in rows
        ]

    async def predict(
        self, session: AsyncSession, student_id: str, problem_id: str
    ) -> dict:
        """Predict P(correct) for a specific problem."""
        # Get primary concept for this problem
        result = await session.execute(
            select(ProblemConcept).where(
                ProblemConcept.problem_id == problem_id,
                ProblemConcept.is_primary == True,  # noqa: E712
            )
        )
        mapping = result.scalar_one_or_none()

        if not mapping:
            return {"p_correct": 0.5, "concept_id": None}

        state = await self.get_or_create_state(
            session, student_id, mapping.concept_id
        )
        params = BKTParams(
            p_l0=state.p_l0,
            p_transit=state.p_transit,
            p_guess=state.p_guess,
            p_slip=state.p_slip,
        )

        p_correct = predict_correctness(state.p_mastery, params)

        return {
            "p_correct": round(p_correct, 4),
            "p_mastery": round(state.p_mastery, 4),
            "concept_id": mapping.concept_id,
        }
