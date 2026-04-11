"""
LLM Hint Generation endpoints.

Layer 5: Socratic hints using LLM + knowledge graph context.
"""

from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, verify_service_key
from app.services.llm_service import generate_hint

router = APIRouter(
    prefix="/hints",
    tags=["hints"],
    dependencies=[Depends(verify_service_key)],
)


class HintRequest(BaseModel):
    student_id: str
    problem_id: str
    code: str = Field(..., max_length=5000)
    error_message: str | None = None
    hint_level: int = Field(default=1, ge=1, le=3)


class HintResponse(BaseModel):
    hint: str | None = None
    hint_level: int = 1
    concepts_referenced: list[str] = []
    tokens_used: int = 0
    error: str | None = None


@router.post("/generate", response_model=HintResponse)
async def get_hint(
    request: HintRequest,
    session: AsyncSession = Depends(get_db_session),
):
    """Generate a Socratic hint for a student's code attempt."""
    result = await generate_hint(
        session=session,
        student_id=request.student_id,
        problem_id=request.problem_id,
        student_code=request.code,
        error_message=request.error_message,
        hint_level=request.hint_level,
    )
    return HintResponse(**result)
