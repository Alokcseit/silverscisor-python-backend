# silverscisor-python/services/skin_tone.py

import os
import numpy as np
import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core import base_options as base_options_lib
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACE_LANDMARKER_MODEL = os.path.join(BASE_DIR, "assets", "models", "face_landmarker_v2.task")


class SkinToneAnalyzer:
    def __init__(self):
        base_opts = base_options_lib.BaseOptions(model_asset_path=FACE_LANDMARKER_MODEL)
        opts = vision.FaceLandmarkerOptions(
            base_options=base_opts,
            running_mode=vision.RunningMode.IMAGE,
            num_faces=1,
        )
        self.face_landmarker = vision.FaceLandmarker.create_from_options(opts)

        # Landmark indices for skin sampling regions
        self.REGIONS = {
            "left_cheek": [116, 117, 118, 119, 120, 123, 50, 205],
            "right_cheek": [345, 346, 347, 348, 349, 352, 280, 425],
            "forehead": [10, 67, 69, 104, 108, 338, 299, 332],
            "nose": [1, 2, 4, 5, 195, 197],
        }

    def get_skin_region(self, img_rgb, landmark_indices, landmarks):
        """Extract skin region pixels around given landmarks"""
        try:
            h, w = img_rgb.shape[:2]
            points = []
            for idx in landmark_indices:
                lm = landmarks[idx]
                x = int(lm.x * w)
                y = int(lm.y * h)
                points.append((x, y))

            xs = [p[0] for p in points]
            ys = [p[1] for p in points]

            margin = 8
            x1 = max(0, min(xs) - margin)
            x2 = min(w, max(xs) + margin)
            y1 = max(0, min(ys) - margin)
            y2 = min(h, max(ys) + margin)

            if x2 <= x1 or y2 <= y1:
                return None
            return img_rgb[y1:y2, x1:x2]
        except Exception:
            return None

    def analyze_skin_tone(self, img_rgb: np.ndarray) -> dict:
        """Skin tone analysis with multiple metrics"""
        try:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
            result = self.face_landmarker.detect(mp_image)

            if not result.face_landmarks:
                print("[SkinTone] No face landmarks found")
                return {"tone": "Medium", "confidence": 50, "details": "Could not detect skin regions"}

            landmarks = result.face_landmarks[0]

            # Extract skin pixels from all regions
            all_pixels = []
            for region_name, indices in self.REGIONS.items():
                region = self.get_skin_region(img_rgb, indices, landmarks)
                if region is not None and region.size > 0:
                    all_pixels.append(region)

            if not all_pixels:
                print("[SkinTone] No skin regions could be extracted")
                return {"tone": "Medium", "confidence": 50, "details": "No skin regions found"}

            combined = np.concatenate([p.reshape(-1, 3) for p in all_pixels], axis=0)
            pixels_uint8 = combined.astype(np.uint8)

            # 1. YCrCb luminance
            ycrcb = cv2.cvtColor(pixels_uint8.reshape(1, -1, 3), cv2.COLOR_RGB2YCrCb)
            y_channel = ycrcb[0, :, 0].flatten()
            avg_y = float(np.mean(y_channel))

            # 2. HSV saturation
            hsv = cv2.cvtColor(pixels_uint8.reshape(1, -1, 3), cv2.COLOR_RGB2HSV)
            h_channel = hsv[0, :, 0].flatten()
            s_channel = hsv[0, :, 1].flatten()
            v_channel = hsv[0, :, 2].flatten()
            avg_h = float(np.mean(h_channel))
            avg_s = float(np.mean(s_channel))
            avg_v = float(np.mean(v_channel))

            # 3. LAB color space
            lab = cv2.cvtColor(pixels_uint8.reshape(1, -1, 3), cv2.COLOR_RGB2Lab)
            l_channel = lab[0, :, 0].flatten()
            a_channel = lab[0, :, 1].flatten()
            b_channel = lab[0, :, 2].flatten()
            avg_l = float(np.mean(l_channel))
            avg_a = float(np.mean(a_channel))
            avg_b_val = float(np.mean(b_channel))

            # Combined score using multiple metrics
            # Luminance (Y from YCrCb, L from Lab) + Hue + Redness (a from Lab)
            brightness_score = (avg_y * 0.5 + avg_l * 0.5)
            warmth_score = avg_a  # positive = redder/warmer

            # Indian skin tones typically range from fair/light to dark/deep
            # Use multiple thresholds for finer classification
            tone = "Medium"
            confidence = 60
            undertone = "Neutral"

            # Determine undertone
            if avg_a > 14:
                undertone = "Warm"
            elif avg_a < 10:
                undertone = "Cool"
            else:
                undertone = "Neutral"

            # Classification based on brightness score (0-255)
            if brightness_score > 185:
                tone = "Fair"
                confidence = 80 + int((brightness_score - 185) / 7)
            elif brightness_score > 160:
                tone = "Light"
                confidence = 75
            elif brightness_score > 130:
                tone = "Medium"
                confidence = 80
            elif brightness_score > 105:
                tone = "Tan"
                confidence = 75
            elif brightness_score > 80:
                tone = "Dark"
                confidence = 80
            else:
                tone = "Deep"
                confidence = 85 + int((80 - brightness_score) / 4)

            confidence = min(98, max(40, confidence))

            # Saturation adjustment - richer skin = more vibrant
            if avg_s > 50:
                tone_quality = "Rich"
            elif avg_s > 30:
                tone_quality = "Natural"
            else:
                tone_quality = "Subtle"

            details = (
                f"{tone_quality} {tone} tone with {undertone.lower()} undertone"
            )

            print(f"[SkinTone] Tone={tone} ({confidence}%), Y={avg_y:.0f}, "
                  f"L={avg_l:.0f}, H={avg_h:.0f}, S={avg_s:.0f}, "
                  f"Undertone={undertone}, Detail='{details}'")

            return {
                "tone": tone,
                "confidence": confidence,
                "undertone": undertone,
                "detail": details,
                "metrics": {
                    "brightness": round(brightness_score, 1),
                    "luminance_y": round(avg_y, 1),
                    "lightness_l": round(avg_l, 1),
                    "redness_a": round(avg_a, 1),
                    "yellowness_b": round(avg_b_val, 1),
                    "hue": round(avg_h, 1),
                    "saturation": round(avg_s, 1),
                    "value": round(avg_v, 1),
                },
            }

        except Exception as e:
            print(f"[SkinTone] Analysis error: {e}")
            return {"tone": "Medium", "confidence": 50, "details": "Analysis error"}


# Singleton
skin_analyzer = SkinToneAnalyzer()
