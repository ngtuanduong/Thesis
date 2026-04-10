"""FastAPI router for Layer 3: Hierarchical Multi-Armed Bandit endpoints."""

from pydantic import BaseModel
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, verify_service_key
from app.services.mab_service import MABService

router = APIRouter(
    prefix="/mab",
    tags=["multi-armed-bandit"],
    dependencies=[Depends(verify_service_key)],
)

mab_service = MABService()


class MABUpdateRequest(BaseModel):
    student_id: str
    concept_id: int
    problem_id: str
    reward: float


@router.post("/select")
async def select_problem(
    student_id: str = Query(...),
    n: int = Query(default=5, ge=1, le=20),
    session: AsyncSession = Depends(get_db_session),
):
    """Select next problem(s) using hierarchical MAB pipeline."""
    return await mab_service.recommend(session, student_id, n)


@router.post("/update")
async def update_mab(
    req: MABUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """Update MAB state after observing a reward."""
    return await mab_service.update(
        session, req.student_id, req.concept_id, req.problem_id, req.reward
    )


@router.get("/practice")
async def select_practice_problem(
    student_id: str = Query(...),
    concept_id: int = Query(...),
    session: AsyncSession = Depends(get_db_session),
):
    """Select the best problem for a specific concept using MAB Thompson Sampling."""
    result = await mab_service._select_problem_for_concept(session, student_id, concept_id)
    if result is None:
        return {"problem_id": None, "title": None, "message": "No eligible problems for this concept"}
    return result


@router.get("/state/{student_id}")
async def get_mab_state(
    student_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    """Get MAB state for debugging/visualization."""
    return await mab_service.get_state(session, student_id)
