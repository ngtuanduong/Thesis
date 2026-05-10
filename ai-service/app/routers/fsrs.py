"""FastAPI router for Layer 4: FSRS Spaced Repetition endpoints."""

from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, verify_service_key
from app.services.fsrs_service import FSRSService

router = APIRouter(
    prefix="/fsrs",
    tags=["spaced-repetition"],
    dependencies=[Depends(verify_service_key)],
)

fsrs_service = FSRSService()


class FSRSReviewRequest(BaseModel):
    student_id: str
    concept_id: int
    rating: int = Field(..., ge=1, le=4)


@router.post("/review")
async def process_review(
    req: FSRSReviewRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """Process a review event and update FSRS card state."""
    return await fsrs_service.review(
        session, req.student_id, req.concept_id, req.rating
    )


@router.get("/queue/{student_id}")
async def get_review_queue(
    student_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    """Get review queue (due + upcoming)."""
    return await fsrs_service.get_review_queue(session, student_id)


@router.get("/card/{student_id}/{concept_id}")
async def get_card(
    student_id: str,
    concept_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    """Get specific FSRS card state."""
    return await fsrs_service.get_card(session, student_id, concept_id)
