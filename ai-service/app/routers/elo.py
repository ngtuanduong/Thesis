"""FastAPI router for Layer 2: Dynamic K-Value Elo Rating endpoints."""

from pydantic import BaseModel
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, verify_service_key
from app.services.elo_service import EloService

router = APIRouter(
    prefix="/elo",
    tags=["elo-rating"],
    dependencies=[Depends(verify_service_key)],
)

elo_service = EloService()


class EloUpdateRequest(BaseModel):
    student_id: str
    problem_id: str
    is_correct: bool
    problem_difficulty: str = "MEDIUM"


@router.post("/update")
async def update_elo(
    req: EloUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """Update Elo ratings after a submission (both student and problem)."""
    return await elo_service.update(
        session,
        req.student_id,
        req.problem_id,
        req.is_correct,
        req.problem_difficulty,
    )


@router.get("/student/{student_id}")
async def get_student_elo(
    student_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    """Get student Elo rating and history."""
    return await elo_service.get_student_elo(session, student_id)


@router.get("/problem/{problem_id}")
async def get_problem_elo(
    problem_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    """Get problem Elo rating."""
    return await elo_service.get_problem_elo(session, problem_id)


@router.get("/zpd/{student_id}")
async def get_zpd_problems(
    student_id: str,
    concept_id: int | None = Query(default=None),
    zpd_min: float = Query(default=100),
    zpd_max: float = Query(default=300),
    session: AsyncSession = Depends(get_db_session),
):
    """Get problems within the student's Zone of Proximal Development."""
    problems = await elo_service.get_zpd_problems(
        session, student_id, concept_id, zpd_min, zpd_max
    )
    return {"student_id": student_id, "zpd_problems": problems}
