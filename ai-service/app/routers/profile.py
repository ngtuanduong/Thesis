from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, verify_service_key
from app.schemas.profile import ProfileResponse, SkillScore

router = APIRouter(prefix="/profile", tags=["profile"], dependencies=[Depends(verify_service_key)])


@router.post("/{user_id}", response_model=ProfileResponse)
async def compute_profile(
    user_id: str,
    request: Request,
    session: AsyncSession = Depends(get_db_session),
):
    profile_service = request.app.state.profile_service
    skills = await profile_service.compute_profile(session, user_id)
    return ProfileResponse(
        user_id=user_id,
        skills=[SkillScore(**s) for s in skills],
    )
