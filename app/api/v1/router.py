from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.habits import router as habits_router
from app.api.v1.recommendations import router as recommendations_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.gamification import router as gamification_router
from app.api.v1.reviews import router as reviews_router
from app.api.v1.coach import router as coach_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(auth_router)
api_v1_router.include_router(habits_router)
api_v1_router.include_router(recommendations_router)
api_v1_router.include_router(analytics_router)
api_v1_router.include_router(gamification_router)
api_v1_router.include_router(reviews_router)
api_v1_router.include_router(coach_router)
