"""
Unified Adaptive Learning endpoints.

These are the primary endpoints that NestJS calls — they orchestrate
all 4 adaptive layers through the AdaptiveEngine.
"""

from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, verify_service_key
from app.services.adaptive_engine import AdaptiveEngine

router = APIRouter(
    prefix="/adaptive",
    tags=["adaptive"],
    dependencies=[Depends(verify_service_key)],
)

engine = AdaptiveEngine()


class SubmissionUpdateRequest(BaseModel):
    student_id: str
    problem_id: str
    is_correct: bool
    attempt_number: int = Field(default=1, ge=1)
    time_spent_seconds: float = Field(default=0, ge=0)


@router.post("/update")
async def update_after_submission(
    req: SubmissionUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """Update all adaptive layers after a submission result."""
    return await engine.process_submission(
        session,
        req.student_id,
        req.problem_id,
        req.is_correct,
        req.attempt_number,
        req.time_spent_seconds,
    )


@router.get("/recommend/{student_id}")
async def get_recommendations(
    student_id: str,
    limit: int = Query(default=5, ge=1, le=20),
    session: AsyncSession = Depends(get_db_session),
):
    """Get adaptive recommendations using all layers."""
    return await engine.get_recommendations(session, student_id, limit)


@router.get("/knowledge-state/{student_id}")
async def get_knowledge_state(
    student_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    """Get complete knowledge state for dashboard visualization."""
    return await engine.get_knowledge_state(session, student_id)


@router.get("/review-queue/{student_id}")
async def get_review_queue(
    student_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    """Get FSRS review queue."""
    return await engine.fsrs.get_review_queue(session, student_id)
