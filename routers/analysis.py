# silverscisor-python/routers/analysis.py

from fastapi import APIRouter, HTTPException
from models.schemas import AnalysisRequest, AnalysisResponse
from services.face_analyzer import face_analyzer
from services.skin_tone import skin_analyzer
from services.recommender import recommender
from utils.image_processor import decode_base64_image, resize_image, convert_bgr_to_rgb
import traceback

router = APIRouter(prefix="/api", tags=["Face Analysis"])


@router.post("/analyze-face", response_model=AnalysisResponse)
async def analyze_face(request: AnalysisRequest):
    """
    Face image analyze karo aur style recommendations do
    """
    try:
        img_bgr = decode_base64_image(request.image)
        img_bgr = resize_image(img_bgr, max_size=640)
        img_rgb = convert_bgr_to_rgb(img_bgr)

        # Face analysis via MediaPipe
        face_result = face_analyzer.analyze(img_rgb)
        if not face_result["success"]:
            raise HTTPException(
                status_code=400,
                detail=face_result.get("error", "Face analysis failed"),
            )

        face_shape = face_result["faceShape"]
        shape_confidence = face_result["faceShapeConfidence"]
        hair_length = face_result["hairLength"]
        face_features = face_result.get("features", {})
        face_details = face_result.get("faceDetails", "")

        # Skin tone analysis
        tone_result = skin_analyzer.analyze_skin_tone(img_rgb)
        skin_tone = tone_result["tone"]
        tone_confidence = tone_result["confidence"]
        undertone = tone_result.get("undertone", "Neutral")
        tone_detail = tone_result.get("detail", "")

        # Recommendations with measurement awareness
        haircuts = recommender.get_haircut_recommendations(
            face_shape, shape_confidence, face_features
        )
        beards = recommender.get_beard_recommendations(
            face_shape, shape_confidence, face_features
        )
        colors = recommender.get_color_recommendations(
            skin_tone, tone_confidence, undertone
        )

        print(f"[Analysis] Shape={face_shape} ({shape_confidence}%), "
              f"Skin={skin_tone} ({tone_confidence}%), "
              f"Hair={hair_length}, Undertone={undertone}")

        return AnalysisResponse(
            success=True,
            data={
                "faceShape": face_shape,
                "faceShapeConfidence": shape_confidence,
                "faceDetails": face_details,
                "skinTone": skin_tone,
                "toneDetail": tone_detail,
                "undertone": undertone,
                "currentHairLength": hair_length,
                "recommendations": {
                    "haircuts": haircuts[:20],
                    "beardStyles": beards[:15],
                    "hairColors": colors[:10],
                },
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Analysis error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")


@router.get("/health")
async def health_check():
    return {
        "success": True,
        "service": "Silverscisor AI Analysis Service",
        "status": "Running",
        "face_analysis": "available",
    }
