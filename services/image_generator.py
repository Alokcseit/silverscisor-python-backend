# silverscisor-python/services/image_generator.py

import os
import io
import base64
import uuid
import requests
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv

load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")

# Replicate model mapping per style type
HAIRCUT_MODEL = "black-forest-labs/flux-dev"       # Best for realistic hair
BEARD_MODEL = "black-forest-labs/flux-dev"
COLOR_MODEL = "black-forest-labs/flux-dev"


def _upload_to_imgbb(image_b64: str) -> str | None:
    """Base64 image ko free image hosting par upload karein"""
    imgbb_key = os.getenv("IMGBB_API_KEY", "")
    if not imgbb_key:
        return None
    try:
        resp = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": imgbb_key, "image": image_b64},
            timeout=15,
        )
        data = resp.json()
        if data.get("success"):
            return data["data"]["url"]
    except Exception as e:
        print(f"[ImgBB] Upload failed: {e}")
    return None


def _save_temp_image(image_b64: str) -> str:
    """Base64 image ko temp file mein save karein"""
    if "," in image_b64:
        image_b64 = image_b64.split(",")[1]
    img_bytes = base64.b64decode(image_b64)
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, f"face_{uuid.uuid4().hex}.jpg")
    with open(filepath, "wb") as f:
        f.write(img_bytes)
    return filepath


def generate_style_image(
    face_image_b64: str,
    style_name: str,
    style_type: str,
    gender: str = "",
) -> str | None:
    """
    Face image + style description → Replicate se AI-generated image
    Returns image URL ya None
    """
    if not REPLICATE_API_TOKEN:
        print("[ImageGen] No REPLICATE_API_TOKEN set, skipping")
        return None

    import replicate

    client = replicate.Client(api_token=REPLICATE_API_TOKEN)

    # Style-specific prompt engineering
    gender_prefix = "man" if gender.lower() in ("male", "man", "") else "woman"

    prompts = {
        "haircuts": f"A {gender_prefix} with {style_name} hairstyle, professional salon photo, well-groomed hair, detailed texture, studio lighting, photorealistic, high quality",
        "beardStyles": f"A {gender_prefix} with {style_name}, well-maintained facial hair, professional grooming, studio lighting, photorealistic, high quality",
        "hairColors": f"A {gender_prefix} with {style_name} hair color, natural looking, salon quality, studio lighting, photorealistic, high quality",
    }

    prompt = prompts.get(style_type, f"A {gender_prefix} with {style_name}, professional photo, high quality")

    try:
        # Save face image to temp file
        temp_path = _save_temp_image(face_image_b64)

        # Upload to Replicate
        with open(temp_path, "rb") as f:
            file_handle = replicate.files.upload(f)

        # Use flux-dev with img2img
        model = HAIRCUT_MODEL
        output = client.run(
            model,
            input={
                "prompt": prompt,
                "image": file_handle,
                "num_outputs": 1,
                "guidance_scale": 3.5,
                "num_inference_steps": 28,
                "strength": 0.75,        # 0.0 = preserve original, 1.0 = completely new
                "aspect_ratio": "3:4",
                "output_format": "jpg",
                "output_quality": 85,
            },
        )

        # Clean up temp file
        try:
            os.remove(temp_path)
        except OSError:
            pass

        if output and len(output) > 0:
            url = str(output[0])
            print(f"[ImageGen] Generated '{style_name}' → {url}")
            return url

    except Exception as e:
        print(f"[ImageGen] Error generating '{style_name}': {e}")

    return None


def generate_multiple_styles(
    face_image_b64: str,
    styles: list[dict],
    gender: str = "",
) -> list[dict]:
    """Multiple styles generate karein (synchronous, sequential)"""
    results = []
    for style in styles:
        url = generate_style_image(
            face_image_b64=face_image_b64,
            style_name=style["name"],
            style_type=style["type"],
            gender=gender,
        )
        results.append({
            "id": style.get("id"),
            "name": style["name"],
            "type": style["type"],
            "image_url": url,
            "generated": url is not None,
        })
    return results
