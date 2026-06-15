# silverscisor-python/services/image_generator.py

import os
import io
import base64
import tempfile
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    tmp.write(img_bytes)
    tmp.close()
    return tmp.name


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
        "haircuts": f"same person with {style_name} hairstyle, same face and features, only hair changed, photorealistic",
        "beardStyles": f"same person with {style_name} facial hair, same face and features, only facial hair changed, photorealistic",
        "hairColors": f"same person with {style_name} hair color, same face and features, only hair color changed, photorealistic",
    }

    prompt = prompts.get(style_type, f"same person with {style_name}, same face and features, only style changed, photorealistic")

    try:
        # Save face image to temp file
        temp_path = _save_temp_image(face_image_b64)

        # Upload to Replicate
        file_handle = client.files.create(temp_path)

        # Use flux-dev with img2img
        model = HAIRCUT_MODEL
        output = client.run(
            model,
            input={
                "prompt": prompt,
                "image": file_handle.urls.get("get"),
                "num_outputs": 1,
                "guidance_scale": 3.5,
                "num_inference_steps": 28,
                "strength": 0.35,        # low = preserve face, only change hair
                "aspect_ratio": "3:4",
                "output_format": "webp",
                "output_quality": 90,
            },
        )

        # Clean up temp file
        try:
            os.remove(temp_path)
        except OSError:
            pass

        if output and len(output) > 0:
            url = str(output[0])
            print(f"[ImageGen] OK '{style_name}' -> {url}")
            return url

    except Exception as e:
        msg = str(e)
        if "429" in msg or "throttled" in msg.lower():
            import time
            print(f"[ImageGen] Rate limited for '{style_name}', retrying in 10s...")
            time.sleep(10)
            try:
                file_handle2 = client.files.create(temp_path)
                output2 = client.run(
                    model,
                    input={
                        "prompt": prompt,
                        "image": file_handle2.urls.get("get"),
                        "num_outputs": 1,
                        "strength": 0.35,
                    },
                )
                if output2 and len(output2) > 0:
                    url = str(output2[0])
                    print(f"[ImageGen] OK (retry) '{style_name}' -> {url}")
                    return url
            except Exception as e2:
                print(f"[ImageGen] Retry also failed for '{style_name}': {e2}")
        else:
            print(f"[ImageGen] Error '{style_name}': {msg[:200]}")

    return None


def generate_multiple_styles(
    face_image_b64: str,
    styles: list[dict],
    gender: str = "",
    max_workers: int = 1,
) -> list[dict]:
    """Multiple styles generate karein (parallel with ThreadPoolExecutor)"""
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                generate_style_image,
                face_image_b64=face_image_b64,
                style_name=style["name"],
                style_type=style["type"],
                gender=gender,
            ): style
            for style in styles
        }
        for future in as_completed(futures):
            style = futures[future]
            try:
                url = future.result()
            except Exception:
                url = None
            results.append({
                "id": style.get("id"),
                "name": style["name"],
                "type": style["type"],
                "image_url": url,
                "generated": url is not None,
            })
    return results
