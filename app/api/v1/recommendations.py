from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.recommendation import RecommendationOut
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["AI Growth Recommendations"])

@router.post("/generate", response_model=RecommendationOut, status_code=status.HTTP_201_CREATED)
async def generate_recommendation(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await RecommendationService.generate_recommendation(db, current_user)

@router.get("/", response_model=list[RecommendationOut])
async def list_recommendations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await RecommendationService.get_user_recommendations(db, current_user.id)
