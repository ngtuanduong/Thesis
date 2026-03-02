"""
Layer 4: FSRS (Free Spaced Repetition Scheduler) Service

Implements FSRS-5 algorithm for scheduling concept reviews to prevent forgetting.
"""

import logging
import math
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tables import Concept, FsrsCard

logger = logging.getLogger(__name__)

# FSRS-5 default parameters (19 weights)
W = [
    0.4072,   # w0: initial stability for rating 1
    1.1829,   # w1: initial stability for rating 2
    3.1262,   # w2: initial stability for rating 3
    15.4722,  # w3: initial stability for rating 4
    7.2102,   # w4: initial difficulty for rating (scale)
    0.5316,   # w5: initial difficulty for rating (offset)
    1.0651,   # w6: difficulty update from rating
    0.0046,   # w7: difficulty mean reversion weight
    1.5401,   # w8: stability after successful recall (base)
    0.1700,   # w9: stability after successful recall (difficulty effect)
    1.0100,   # w10: stability after successful recall (stability effect)
    2.0700,   # w11: stability after successful recall (retrievability effect)
    0.0500,   # w12: stability after failure (base)
    0.3600,   # w13: stability after failure (difficulty effect)
    0.1500,   # w14: stability after failure (stability effect)
    0.2100,   # w15: stability after failure (retrievability effect)
    0.0500,   # w16: stability after failure (minimum factor)
    2.5000,   # w17: hard penalty
    0.2700,   # w18: easy bonus
]


def fsrs_initial_stability(rating: int) -> float:
    """Initial stability based on first rating."""
    return W[max(0, min(3, rating - 1))]


def fsrs_initial_difficulty(rating: int) -> float:
    """Initial difficulty based on first rating."""
    d = W[4] - math.exp(W[5] * (rating - 1)) + 1
    return max(1.0, min(10.0, d))


def fsrs_update_difficulty(d: float, rating: int) -> float:
    """Update difficulty after a review."""
    d_new = d - W[6] * (rating - 3)
    d_new = W[7] * fsrs_initial_difficulty(3) + (1 - W[7]) * d_new
    return max(1.0, min(10.0, d_new))


def fsrs_stability_success(d: float, s: float, r: float, rating: int) -> float:
    """Update stability after successful recall (rating >= 2)."""
    hard_penalty = W[17] if rating == 2 else 1.0
    easy_bonus = W[18] if rating == 4 else 1.0

    s_new = s * (
        1 + math.exp(W[8])
        * (11 - d) ** W[9]
        * s ** (-W[10])
        * (math.exp((1 - r) * W[11]) - 1)
        * hard_penalty
        * easy_bonus
    )
    return max(0.1, s_new)


def fsrs_stability_fail(d: float, s: float, r: float) -> float:
    """Update stability after failed recall (rating = 1)."""
    s_new = (
        W[12]
        * d ** (-W[13])
        * ((s + 1) ** W[14] - 1)
        * math.exp((1 - r) * W[15])
    )
    return max(0.1, min(s, s_new))


def compute_retrievability(elapsed_days: float, stability: float) -> float:
    """Compute current retrievability using power-law decay."""
    if stability <= 0:
        return 0.0
    return (1 + elapsed_days / (9 * stability)) ** (-1)


def submission_to_fsrs_rating(
    is_correct: bool, attempt_number: int, time_spent_seconds: float
) -> int:
    """Map a programming submission outcome to an FSRS rating (1-4)."""
    if not is_correct:
        return 1  # Again

    if attempt_number == 1:
        if time_spent_seconds < 120:
            return 4  # Easy
        elif time_spent_seconds < 300:
            return 3  # Good
        else:
            return 2  # Hard
    elif attempt_number <= 3:
        return 2  # Hard
    else:
        return 2  # Hard


class FSRSService:
    """Service for FSRS spaced repetition operations."""

    async def get_or_create_card(
        self, session: AsyncSession, student_id: str, concept_id: int
    ) -> FsrsCard:
        """Get existing FSRS card or create a new one."""
        result = await session.execute(
            select(FsrsCard).where(
                FsrsCard.student_id == student_id,
                FsrsCard.concept_id == concept_id,
            )
        )
        card = result.scalar_one_or_none()

        if card is None:
            card = FsrsCard(
                student_id=student_id,
                concept_id=concept_id,
                difficulty=5.0,
                stability=1.0,
                retrievability=1.0,
                state="NEW",
                due_date=datetime.utcnow(),
                reps=0,
                lapses=0,
            )
            session.add(card)
            await session.flush()

        return card

    async def review(
        self,
        session: AsyncSession,
        student_id: str,
        concept_id: int,
        rating: int,
    ) -> dict:
        """
        Process a review event for an FSRS card.
        Rating: 1=Again, 2=Hard, 3=Good, 4=Easy
        """
        card = await self.get_or_create_card(session, student_id, concept_id)
        now = datetime.utcnow()

        stability_before = card.stability
        difficulty_before = card.difficulty

        if card.state == "NEW":
            # First review
            card.difficulty = fsrs_initial_difficulty(rating)
            card.stability = fsrs_initial_stability(rating)
            card.state = "LEARNING" if rating < 3 else "REVIEW"
        else:
            # Calculate current retrievability
            if card.last_review:
                elapsed_days = (now - card.last_review).total_seconds() / 86400
            else:
                elapsed_days = 0.0
            r = compute_retrievability(elapsed_days, card.stability)

            # Update difficulty
            card.difficulty = fsrs_update_difficulty(card.difficulty, rating)

            if rating == 1:
                # Failed recall
                card.stability = fsrs_stability_fail(card.difficulty, card.stability, r)
                card.lapses += 1
                card.state = "RELEARNING"
            else:
                # Successful recall
                card.stability = fsrs_stability_success(
                    card.difficulty, card.stability, r, rating
                )
                card.state = "REVIEW"

        card.reps += 1
        card.last_review = now
        card.retrievability = 1.0  # Just reviewed

        # Schedule next review: when R will drop to 0.9
        # R(t) = (1 + t/(9S))^(-1) = 0.9  →  t = S
        card.due_date = now + timedelta(days=card.stability)

        await session.commit()

        return {
            "concept_id": concept_id,
            "rating": rating,
            "difficulty_before": round(difficulty_before, 4),
            "difficulty_after": round(card.difficulty, 4),
            "stability_before": round(stability_before, 4),
            "stability_after": round(card.stability, 4),
            "state": card.state,
            "next_review": card.due_date.isoformat(),
            "reps": card.reps,
            "lapses": card.lapses,
        }

    async def get_review_queue(
        self, session: AsyncSession, student_id: str
    ) -> dict:
        """Get concepts due for review, ordered by urgency."""
        result = await session.execute(
            select(FsrsCard, Concept)
            .join(Concept, FsrsCard.concept_id == Concept.id)
            .where(
                FsrsCard.student_id == student_id,
                FsrsCard.state != "NEW",
            )
        )
        rows = result.all()
        now = datetime.utcnow()

        due_cards = []
        upcoming_cards = []

        for card, concept in rows:
            if card.last_review:
                elapsed_days = (now - card.last_review).total_seconds() / 86400
            else:
                elapsed_days = 0.0

            current_r = compute_retrievability(elapsed_days, card.stability)

            if current_r < 0.9:
                due_date = card.due_date if card.due_date.tzinfo is None else card.due_date
                due_cards.append({
                    "concept_id": card.concept_id,
                    "concept_name": concept.name,
                    "display_name": concept.display_name,
                    "retrievability": round(current_r, 4),
                    "due_date": due_date.isoformat() if due_date else None,
                    "days_overdue": max(0, (now - due_date).days),
                    "urgency": round(1.0 - current_r, 4),
                    "stability": round(card.stability, 2),
                    "difficulty": round(card.difficulty, 2),
                    "state": card.state,
                })
            elif card.due_date:
                due_date = card.due_date if card.due_date.tzinfo is None else card.due_date
                if due_date <= now + timedelta(days=3):
                    upcoming_cards.append({
                        "concept_id": card.concept_id,
                        "concept_name": concept.name,
                        "display_name": concept.display_name,
                        "due_date": due_date.isoformat(),
                        "retrievability": round(current_r, 4),
                        "stability": round(card.stability, 2),
                        "difficulty": round(card.difficulty, 2),
                        "state": card.state,
                    })

        due_cards.sort(key=lambda x: x["retrievability"])
        upcoming_cards.sort(key=lambda x: x["due_date"])

        return {"due_now": due_cards, "upcoming": upcoming_cards}

    async def get_card(
        self, session: AsyncSession, student_id: str, concept_id: int
    ) -> dict | None:
        """Get specific card state."""
        card = await self.get_or_create_card(session, student_id, concept_id)
        now = datetime.utcnow()

        if card.last_review:
            elapsed_days = (now - card.last_review).total_seconds() / 86400
            current_r = compute_retrievability(elapsed_days, card.stability)
        else:
            current_r = card.retrievability

        return {
            "concept_id": card.concept_id,
            "difficulty": round(card.difficulty, 4),
            "stability": round(card.stability, 4),
            "retrievability": round(current_r, 4),
            "state": card.state,
            "due_date": card.due_date.isoformat() if card.due_date else None,
            "last_review": card.last_review.isoformat() if card.last_review else None,
            "reps": card.reps,
            "lapses": card.lapses,
        }
