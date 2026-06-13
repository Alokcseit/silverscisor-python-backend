# silverscisor-python/models/schemas.py

from pydantic import BaseModel
from typing import List, Optional


class AnalysisRequest(BaseModel):
    image: str  # base64 encoded image


class StyleItem(BaseModel):
    id: int
    name: str
    confidence: int
    description: str
    price: int
    duration: str
    tags: List[str]
    image: Optional[str] = None


class ColorItem(BaseModel):
    id: int
    name: str
    confidence: int
    description: str
    colorCode: str
    price: int
    duration: str
    tags: List[str]
    image: Optional[str] = None


class Recommendations(BaseModel):
    haircuts: List[StyleItem]
    beardStyles: List[StyleItem]
    hairColors: List[ColorItem]


class AnalysisResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    message: Optional[str] = None


class RecommendationRequest(BaseModel):
    userId: str
    bookingHistory: Optional[List[dict]] = []
    location: Optional[str] = ""


class TrendingRequest(BaseModel):
    city: Optional[str] = "default"