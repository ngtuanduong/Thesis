from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, verify_service_key
from app.schemas.skill_gap import SkillGapItem, SkillGapResponse
from app.services.skill_gap_service import SkillGapService

router = APIRouter(prefix="/skill-gap", tags=["skill-gap"], dependencies=[Depends(verify_service_key)])

skill_gap_service = SkillGapService()


@router.get("/{user_id}", response_model=SkillGapResponse)
async def analyze_skill_gap(
    user_id: str,
    session: AsyncSession = Depends(get_db_session),
):
    gaps = await skill_gap_service.analyze(session, user_id)
    return SkillGapResponse(
        user_id=user_id,
        gaps=[SkillGapItem(**g) for g in gaps],
    )
