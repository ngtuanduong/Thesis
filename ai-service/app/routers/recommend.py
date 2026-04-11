from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, verify_service_key
from app.schemas.recommendation import RecommendationsResponse, RecommendedProblem
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommend", tags=["recommendations"], dependencies=[Depends(verify_service_key)])

recommendation_service = RecommendationService()


@router.get("/{user_id}", response_model=RecommendationsResponse)
async def get_recommendations(
    user_id: str,
    limit: int = Query(default=10, ge=1, le=50),
    session: AsyncSession = Depends(get_db_session),
):
    results = await recommendation_service.get_recommendations(session, user_id, limit)
    return RecommendationsResponse(
        user_id=user_id,
        recommendations=[RecommendedProblem(**r) for r in results],
    )
