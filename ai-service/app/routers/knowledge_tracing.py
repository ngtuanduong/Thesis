"""FastAPI router for Layer 1: BKT Knowledge Tracing endpoints."""

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, verify_service_key
from app.services.bkt_service import BKTService

router = APIRouter(
    prefix="/kt",
    tags=["knowledge-tracing"],
    dependencies=[Depends(verify_service_key)],
)

bkt_service = BKTService()


class KTUpdateRequest(BaseModel):
    student_id: str
    problem_id: str
    is_correct: bool


class KTPredictResponse(BaseModel):
    p_correct: float
    p_mastery: float
    concept_id: int | None


@router.post("/update")
async def update_knowledge(
    req: KTUpdateRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """Update BKT knowledge state after a submission."""
    return await bkt_service.update(
        session, req.student_id, req.problem_id, req.is_correct
    )


@router.get("/state/{student_id}")
async def get_knowledge_state(
    student_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    """Get all knowledge states for a student."""
    states = await bkt_service.get_state(session, student_id)
    return {"student_id": student_id, "states": states}


@router.get("/predict/{student_id}/{problem_id}", response_model=KTPredictResponse)
async def predict_correctness(
    student_id: str,
    problem_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    """Predict P(correct) for a student on a specific problem."""
    return await bkt_service.predict(session, student_id, problem_id)
