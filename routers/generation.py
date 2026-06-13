# silverscisor-python/routers/generation.py

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from services.image_generator import generate_multiple_styles, generate_style_image

router = APIRouter(prefix="/api", tags=["AI Image Generation"])


class StyleImageRequest(BaseModel):
    image: str  # base64 encoded face image
    styles: List[dict]  # [{id, name, type}, ...]
    gender: Optional[str] = ""


class StyleImageResponse(BaseModel):
    success: bool
    images: Optional[List[dict]] = None
    message: Optional[str] = None


@router.post("/generate-style-images", response_model=StyleImageResponse)
async def generate_style_images(req: StyleImageRequest):
    """
    Face image + style list → AI-generated images
    Har style ka realistic photo banata hai using Replicate
    """
    has_api_key = bool(os.getenv("REPLICATE_API_TOKEN", ""))
    if not has_api_key:
        return StyleImageResponse(
            success=False,
            message="AI image generation not configured. Set REPLICATE_API_TOKEN in .env",
        )

    try:
        images = generate_multiple_styles(
            face_image_b64=req.image,
            styles=req.styles,
            gender=req.gender,
        )

        generated_count = sum(1 for img in images if img["generated"])
        failed_count = len(images) - generated_count

        return StyleImageResponse(
            success=True,
            images=images,
            message=f"Generated {generated_count}/{len(images)} images{' (' + str(failed_count) + ' failed)' if failed_count else ''}",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")
