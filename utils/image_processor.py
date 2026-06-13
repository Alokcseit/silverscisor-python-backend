# silverscisor-python/utils/image_processor.py

import base64
import numpy as np
import cv2
from PIL import Image
import io


def decode_base64_image(base64_string: str) -> np.ndarray:
    """Base64 string ko OpenCV image mein convert karo"""
    try:
        # Remove data URL prefix if present
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        # Decode base64
        img_bytes = base64.b64decode(base64_string)

        # Convert to numpy array
        nparr = np.frombuffer(img_bytes, np.uint8)

        # Decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Could not decode image")

        return img

    except Exception as e:
        raise ValueError(f"Image decode failed: {str(e)}")


def resize_image(img: np.ndarray, max_size: int = 640) -> np.ndarray:
    """Image ko resize karo processing ke liye"""
    h, w = img.shape[:2]

    if max(h, w) <= max_size:
        return img

    scale = max_size / max(h, w)
    new_w = int(w * scale)
    new_h = int(h * scale)

    return cv2.resize(img, (new_w, new_h))


def convert_bgr_to_rgb(img: np.ndarray) -> np.ndarray:
    """OpenCV BGR ko RGB mein convert karo"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def get_image_dimensions(img: np.ndarray) -> tuple:
    """Image dimensions return karo"""
    h, w = img.shape[:2]
    return w, h