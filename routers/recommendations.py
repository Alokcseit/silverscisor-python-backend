# silverscisor-python/routers/recommendations.py

from fastapi import APIRouter
from models.schemas import RecommendationRequest, TrendingRequest
from services.recommender import recommender

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])


@router.get("/user/{user_id}")
async def get_user_recommendations(user_id: str):
    """User ke liye personalized recommendations"""
    result = recommender.get_user_recommendations(user_id, [])
    return {"success": True, "data": result}


@router.post("/user/{user_id}")
async def get_personalized_recommendations(user_id: str, request: RecommendationRequest):
    """History-based personalized recommendations"""
    result = recommender.get_user_recommendations(
        user_id,
        request.bookingHistory
    )
    return {"success": True, "data": result}


@router.get("/trending")
async def get_trending(city: str = "default"):
    """Trending services in city"""
    trending = recommender.get_trending(city)
    return {
        "success": True,
        "data": {"trending": trending}
    }