"""
Layer 2: Dynamic K-Value Elo Rating Service

Implements dual Elo system (student + problem ratings) with dynamic K-factor
and Zone of Proximal Development (ZPD) filtering.
"""

import json
import logging
import math
from datetime import datetime, timezone

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tables import EloRating, ProblemConcept

logger = logging.getLogger(__name__)

# Elo constants
DEFAULT_STUDENT_ELO = 1200.0
ELO_INIT = {"EASY": 1000.0, "MEDIUM": 1400.0, "HARD": 1800.0}
ELO_MIN = 400.0
ELO_MAX = 2800.0
K_MIN = 10.0
K_MAX = 40.0
TREND_WINDOW = 10
TREND_LAMBDA = 2.0


def expected_score(r_student: float, r_problem: float) -> float:
    """Compute expected probability of student solving the problem."""
    return 1.0 / (1.0 + 10 ** ((r_problem - r_student) / 400))


def compute_dynamic_k(history: list[dict], k_min=K_MIN, k_max=K_MAX) -> float:
    """
    Compute dynamic K-value based on recent performance trend.

    Higher K = faster calibration (for struggling/new students).
    Lower K = more stable (for consistently performing students).
    """
    if len(history) < 3:
        return k_max  # New students get high K for fast initial calibration

    recent = history[-TREND_WINDOW:]

    # Weighted trend: sum of (actual - expected) with exponential recency
    trend = 0.0
    total_weight = 0.0
    for i, h in enumerate(recent):
        weight = 0.9 ** (len(recent) - 1 - i)
        actual = 1.0 if h.get("is_correct") else 0.0
        residual = actual - h.get("expected_score", 0.5)
        trend += weight * residual
        total_weight += weight

    if total_weight > 0:
        trend = trend / total_weight

    if trend > 0:
        # Improving → lower K (stable)
        k = k_min + (k_max - k_min) * math.exp(-TREND_LAMBDA * trend)
    else:
        # Struggling → higher K (needs re-calibration)
        k = k_min + (k_max - k_min) * (1 - math.exp(TREND_LAMBDA * trend))

    return k


def compute_problem_k(n_attempts: int) -> float:
    """Problem K decreases as more students attempt it."""
    return max(K_MIN, K_MAX / math.sqrt(max(1, n_attempts)))


class EloService:
    """Service for Elo rating operations."""

    async def get_or_create_rating(
        self,
        session: AsyncSession,
        entity_id: str,
        entity_type: str,
        initial_rating: float = DEFAULT_STUDENT_ELO,
        concept_id: int | None = None,
    ) -> EloRating:
        """Get existing Elo rating or create with defaults."""
        conditions = [
            EloRating.entity_id == entity_id,
            EloRating.entity_type == entity_type,
        ]
        if concept_id is not None:
            conditions.append(EloRating.concept_id == concept_id)
        else:
            conditions.append(EloRating.concept_id.is_(None))

        result = await session.execute(
            select(EloRating).where(and_(*conditions))
        )
        rating = result.scalar_one_or_none()

        if rating is None:
            rating = EloRating(
                entity_id=entity_id,
                entity_type=entity_type,
                concept_id=concept_id,
                rating=initial_rating,
                k_value=K_MAX,
                trend=0.0,
                n_attempts=0,
                rating_history=json.dumps([]),
            )
            session.add(rating)
            await session.flush()

        return rating

    async def update(
        self,
        session: AsyncSession,
        student_id: str,
        problem_id: str,
        is_correct: bool,
        problem_difficulty: str = "MEDIUM",
    ) -> dict:
        """
        Full Elo update after a submission.
        Updates both student and problem ratings with dynamic K.
        """
        # Get or create ratings
        student_elo = await self.get_or_create_rating(
            session, student_id, "STUDENT", DEFAULT_STUDENT_ELO
        )
        problem_elo = await self.get_or_create_rating(
            session, problem_id, "PROBLEM", ELO_INIT.get(problem_difficulty, 1400.0)
        )

        # Expected score
        exp = expected_score(student_elo.rating, problem_elo.rating)
        actual = 1.0 if is_correct else 0.0

        # Parse rating history
        try:
            student_history = json.loads(student_elo.rating_history) if isinstance(student_elo.rating_history, str) else student_elo.rating_history or []
        except (json.JSONDecodeError, TypeError):
            student_history = []

        # Dynamic K for student
        k_student = compute_dynamic_k(student_history)

        # Problem K decreases with more data
        k_problem = compute_problem_k(problem_elo.n_attempts)

        # Store before values
        student_before = student_elo.rating
        problem_before = problem_elo.rating

        # Update ratings
        student_elo.rating += k_student * (actual - exp)
        problem_elo.rating += k_problem * (exp - actual)

        # Clamp
        student_elo.rating = max(ELO_MIN, min(ELO_MAX, student_elo.rating))
        problem_elo.rating = max(ELO_MIN, min(ELO_MAX, problem_elo.rating))

        # Update metadata
        student_elo.n_attempts += 1
        problem_elo.n_attempts += 1
        student_elo.k_value = k_student

        # Append to history
        history_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "rating": round(student_elo.rating, 1),
            "opponent_rating": round(problem_elo.rating, 1),
            "outcome": actual,
            "expected_score": round(exp, 4),
            "is_correct": is_correct,
        }
        student_history.append(history_entry)
        # Keep last 100 entries
        if len(student_history) > 100:
            student_history = student_history[-100:]
        student_elo.rating_history = json.dumps(student_history)

        # Compute trend
        if len(student_history) >= 3:
            recent = student_history[-TREND_WINDOW:]
            trend = sum(
                (1.0 if h.get("is_correct") else 0.0) - h.get("expected_score", 0.5)
                for h in recent
            ) / len(recent)
            student_elo.trend = round(trend, 4)

        await session.commit()

        return {
            "student_elo_before": round(student_before, 1),
            "student_elo_after": round(student_elo.rating, 1),
            "problem_elo_before": round(problem_before, 1),
            "problem_elo_after": round(problem_elo.rating, 1),
            "expected": round(exp, 4),
            "k_student": round(k_student, 1),
            "k_problem": round(k_problem, 1),
        }

    async def get_student_elo(
        self, session: AsyncSession, student_id: str
    ) -> dict:
        """Get student Elo rating and history."""
        rating = await self.get_or_create_rating(
            session, student_id, "STUDENT"
        )

        try:
            history = json.loads(rating.rating_history) if isinstance(rating.rating_history, str) else rating.rating_history or []
        except (json.JSONDecodeError, TypeError):
            history = []

        return {
            "entity_id": student_id,
            "entity_type": "STUDENT",
            "rating": round(rating.rating, 1),
            "k_value": round(rating.k_value, 1),
            "trend": round(rating.trend, 4),
            "n_attempts": rating.n_attempts,
            "history": history[-20:],  # Last 20 for display
        }

    async def get_problem_elo(
        self, session: AsyncSession, problem_id: str
    ) -> dict:
        """Get problem Elo rating."""
        rating = await self.get_or_create_rating(
            session, problem_id, "PROBLEM"
        )
        return {
            "entity_id": problem_id,
            "entity_type": "PROBLEM",
            "rating": round(rating.rating, 1),
            "n_attempts": rating.n_attempts,
        }

    async def get_zpd_problems(
        self,
        session: AsyncSession,
        student_id: str,
        concept_id: int | None = None,
        zpd_min: float = 100,
        zpd_max: float = 300,
    ) -> list[dict]:
        """
        Get problems within the student's Zone of Proximal Development.
        ZPD = [student_elo + zpd_min, student_elo + zpd_max]
        Maps to ~36-64% expected success rate.
        """
        student_rating = await self.get_or_create_rating(
            session, student_id, "STUDENT"
        )
        target_min = student_rating.rating + zpd_min
        target_max = student_rating.rating + zpd_max

        # Query problem Elo ratings in range
        query = select(EloRating).where(
            EloRating.entity_type == "PROBLEM",
            EloRating.rating >= target_min,
            EloRating.rating <= target_max,
        )
        result = await session.execute(query)
        problem_elos = result.scalars().all()

        # If concept_id specified, filter by concept
        if concept_id is not None and problem_elos:
            concept_result = await session.execute(
                select(ProblemConcept.problem_id).where(
                    ProblemConcept.concept_id == concept_id
                )
            )
            concept_problem_ids = {str(row[0]) for row in concept_result.all()}
            problem_elos = [
                pe for pe in problem_elos if str(pe.entity_id) in concept_problem_ids
            ]

        problems = [
            {
                "problem_id": str(pe.entity_id),
                "problem_elo": round(pe.rating, 1),
                "expected_success": round(
                    expected_score(student_rating.rating, pe.rating), 4
                ),
                "difficulty_match": round(
                    1.0 - abs(pe.rating - student_rating.rating - 200) / 400, 4
                ),
            }
            for pe in problem_elos
        ]

        # If no problems in ZPD, expand range
        if not problems:
            query_expanded = select(EloRating).where(
                EloRating.entity_type == "PROBLEM",
                EloRating.rating >= student_rating.rating,
                EloRating.rating <= student_rating.rating + 400,
            )
            result = await session.execute(query_expanded)
            expanded_elos = result.scalars().all()

            if concept_id is not None and expanded_elos:
                expanded_elos = [
                    pe for pe in expanded_elos
                    if str(pe.entity_id) in concept_problem_ids
                ]

            problems = [
                {
                    "problem_id": str(pe.entity_id),
                    "problem_elo": round(pe.rating, 1),
                    "expected_success": round(
                        expected_score(student_rating.rating, pe.rating), 4
                    ),
                    "difficulty_match": round(
                        1.0 - abs(pe.rating - student_rating.rating - 200) / 400, 4
                    ),
                }
                for pe in expanded_elos
            ]

        return problems
