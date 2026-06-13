# silverscisor-python/services/face_analyzer.py

import os
import math
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core import base_options as base_options_lib
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACE_LANDMARKER_MODEL = os.path.join(BASE_DIR, "assets", "models", "face_landmarker_v2.task")
FACE_DETECTOR_MODEL = os.path.join(BASE_DIR, "assets", "models", "face_detection_short_range.tflite")

# FaceMesh landmark indices for key facial features
LM = {
    "forehead_top": 10,
    "chin_bottom": 152,
    "left_temple": 103,
    "right_temple": 332,
    "left_cheek": 234,
    "right_cheek": 454,
    "left_jaw": 172,
    "right_jaw": 397,
    "chin_left": 175,
    "chin_right": 395,
    "nose_bridge_top": 168,
    "nose_bridge_bottom": 6,
    "left_eye_outer": 66,
    "right_eye_outer": 296,
    "left_eyebrow_center": 70,
    "right_eyebrow_center": 300,
}

# Ideal ratio profiles for each face shape
# Format: (length/width, forehead/cheek, jaw/cheek, forehead/jaw)
SHAPE_PROFILES = {
    "Oval":     [1.35, 0.92, 0.82, 1.12],
    "Round":    [1.10, 0.95, 0.88, 1.08],
    "Square":   [1.20, 0.92, 0.90, 1.02],
    "Heart":    [1.30, 0.98, 0.75, 1.30],
    "Oblong":   [1.55, 0.88, 0.80, 1.10],
    "Diamond":  [1.40, 0.85, 0.75, 1.13],
    "Triangle": [1.25, 0.85, 0.95, 0.89],
}

# Weights for each ratio in distance calculation
RATIO_WEIGHTS = [0.35, 0.20, 0.25, 0.20]


class FaceAnalyzer:
    def __init__(self):
        base_opts_lm = base_options_lib.BaseOptions(model_asset_path=FACE_LANDMARKER_MODEL)
        opts_lm = vision.FaceLandmarkerOptions(
            base_options=base_opts_lm,
            running_mode=vision.RunningMode.IMAGE,
            num_faces=1,
        )
        self.face_landmarker = vision.FaceLandmarker.create_from_options(opts_lm)

        base_opts_fd = base_options_lib.BaseOptions(model_asset_path=FACE_DETECTOR_MODEL)
        opts_fd = vision.FaceDetectorOptions(
            base_options=base_opts_fd,
            running_mode=vision.RunningMode.IMAGE,
            min_detection_confidence=0.5,
        )
        self.face_detector = vision.FaceDetector.create_from_options(opts_fd)

    def detect_face(self, img_rgb: np.ndarray) -> bool:
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        result = self.face_detector.detect(mp_image)
        return len(result.detections) > 0

    def get_landmarks(self, img_rgb: np.ndarray) -> Optional[list]:
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        result = self.face_landmarker.detect(mp_image)
        if not result.face_landmarks:
            return None
        h, w = img_rgb.shape[:2]
        points = [(int(lm.x * w), int(lm.y * h)) for lm in result.face_landmarks[0]]
        return points

    def _distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def extract_face_measurements(self, landmarks: list):
        """Extract precise face measurements from landmarks"""
        pts = {}
        for name, idx in LM.items():
            pts[name] = landmarks[idx]

        # Core distances
        face_length = self._distance(pts["forehead_top"], pts["chin_bottom"])
        forehead_width = self._distance(pts["left_temple"], pts["right_temple"])
        cheek_width = self._distance(pts["left_cheek"], pts["right_cheek"])
        jaw_width = self._distance(pts["left_jaw"], pts["right_jaw"])
        chin_width = self._distance(pts["chin_left"], pts["chin_right"])

        # Derived ratios
        ratios = {
            "length_width": face_length / cheek_width if cheek_width else 1,
            "forehead_cheek": forehead_width / cheek_width if cheek_width else 1,
            "jaw_cheek": jaw_width / cheek_width if cheek_width else 1,
            "forehead_jaw": forehead_width / jaw_width if jaw_width else 1,
            "jaw_forehead": jaw_width / forehead_width if forehead_width else 1,
            "chin_cheek": chin_width / cheek_width if cheek_width else 1,
        }

        # Feature descriptions
        features = {
            "jaw_type": self._classify_jaw(jaw_width, cheek_width, chin_width),
            "forehead_type": self._classify_forehead(forehead_width, cheek_width),
            "cheek_type": self._classify_cheeks(cheek_width, forehead_width, jaw_width),
            "chin_type": self._classify_chin(chin_width, jaw_width),
            "face_balance": round(ratios["length_width"], 2),
        }

        raw = {k: round(v, 1) for k, v in {
            "face_length": face_length,
            "forehead_width": forehead_width,
            "cheek_width": cheek_width,
            "jaw_width": jaw_width,
            "chin_width": chin_width,
        }.items()}

        return ratios, features, raw

    def _classify_jaw(self, jaw_width, cheek_width, chin_width):
        ratio = jaw_width / cheek_width if cheek_width else 0
        if ratio > 0.90:
            return "Strong square"
        elif ratio > 0.82:
            return "Balanced"
        elif ratio > 0.72:
            return "Soft rounded"
        else:
            return "Narrow pointed"

    def _classify_forehead(self, forehead_width, cheek_width):
        ratio = forehead_width / cheek_width if cheek_width else 0
        if ratio > 0.97:
            return "Wide"
        elif ratio > 0.88:
            return "Balanced"
        else:
            return "Narrow"

    def _classify_cheeks(self, cheek_width, forehead_width, jaw_width):
        f_ratio = cheek_width / forehead_width if forehead_width else 0
        j_ratio = cheek_width / jaw_width if jaw_width else 0
        if f_ratio > 1.12 and j_ratio > 1.15:
            return "Prominent cheekbones"
        elif f_ratio > 1.05 or j_ratio > 1.08:
            return "Full"
        elif f_ratio < 0.95 and j_ratio < 0.95:
            return "Flat"
        else:
            return "Balanced"

    def _classify_chin(self, chin_width, jaw_width):
        ratio = chin_width / jaw_width if jaw_width else 0
        if ratio > 0.70:
            return "Rounded"
        elif ratio > 0.50:
            return "Balanced"
        else:
            return "Pointed"

    def calculate_face_shape(self, landmarks: list) -> dict:
        """Face shape classify using distance-weighted profile matching"""
        ratios, features, raw = self.extract_face_measurements(landmarks)

        actual = [
            ratios["length_width"],
            ratios["forehead_cheek"],
            ratios["jaw_cheek"],
            ratios["forehead_jaw"],
        ]

        results = []
        for shape_name, ideal in SHAPE_PROFILES.items():
            weight_dist = 0
            for i in range(4):
                diff = abs(actual[i] - ideal[i])
                weight_dist += diff * RATIO_WEIGHTS[i]

            score = max(0, min(100, int((1.0 - weight_dist / 0.5) * 100)))
            results.append((shape_name, score, weight_dist))

        results.sort(key=lambda x: -x[1])
        best_shape, best_score, _ = results[0]

        # If best score is very low, check stricter conditions
        if best_score < 30:
            lw = ratios["length_width"]
            if lw >= 1.5:
                best_shape = "Oblong"
            elif lw < 1.15 and ratios["forehead_jaw"] < 1.15:
                best_shape = "Round"
            elif ratios["jaw_forehead"] > 0.95:
                best_shape = "Square"
            elif ratios["forehead_jaw"] > 1.25:
                best_shape = "Heart"

        # Detailed features description
        jaw_desc = features["jaw_type"]
        forehead_desc = features["forehead_type"]
        cheek_desc = features["cheek_type"]
        chin_desc = features["chin_type"]

        details = (
            f"{jaw_desc} jawline, {forehead_desc} forehead, "
            f"{cheek_desc} cheeks, {chin_desc} chin"
        )

        return {
            "shape": best_shape,
            "confidence": best_score,
            "ratios": {k: round(v, 2) for k, v in ratios.items()},
            "measurements": raw,
            "features": features,
            "details": details,
            "all_scores": {s: sc for s, sc, _ in results},
        }

    def get_hair_length_estimate(self, landmarks: list, img_height: int) -> tuple:
        """Hair length estimate with confidence"""
        try:
            forehead_top = landmarks[LM["forehead_top"]]
            chin = landmarks[LM["chin_bottom"]]

            face_height = abs(chin[1] - forehead_top[1])
            top_margin = forehead_top[1]

            ratio = top_margin / face_height if face_height > 0 else 1

            if ratio < -0.3:
                return "Very Long", 95
            elif ratio < 0.1:
                return "Long", 88
            elif ratio < 0.4:
                return "Medium", 80
            elif ratio < 0.7:
                return "Short", 85
            else:
                return "Very Short", 90
        except IndexError:
            return "Short", 50

    def analyze(self, img_rgb: np.ndarray) -> dict:
        """Complete face analysis with detailed measurements"""
        h, w = img_rgb.shape[:2]

        has_face = self.detect_face(img_rgb)
        if not has_face:
            print("[FaceAnalyzer] No face detected in image")
            return {"success": False, "error": "No face detected"}

        landmarks = self.get_landmarks(img_rgb)
        if landmarks is None or len(landmarks) < 478:
            print(f"[FaceAnalyzer] Insufficient landmarks: {len(landmarks) if landmarks else 0}")
            return {"success": False, "error": "Could not analyze face features"}

        face_result = self.calculate_face_shape(landmarks)
        hair_length, hair_conf = self.get_hair_length_estimate(landmarks, h)

        shape_name = face_result["shape"]
        shape_conf = face_result["confidence"]

        print(f"[FaceAnalyzer] Shape={shape_name} ({shape_conf}%), "
              f"Hair={hair_length} ({hair_conf}%), "
              f"Bal={face_result['ratios']['length_width']}, "
              f"Jaw/Cheek={face_result['ratios']['jaw_cheek']}, "
              f"For/Jaw={face_result['ratios']['forehead_jaw']}")

        return {
            "success": True,
            "faceShape": shape_name,
            "faceShapeConfidence": shape_conf,
            "hairLength": hair_length,
            "hairConfidence": hair_conf,
            "faceDetails": face_result["details"],
            "measurements": face_result["measurements"],
            "ratios": face_result["ratios"],
            "features": face_result["features"],
            "allScores": face_result["all_scores"],
        }


# Singleton
face_analyzer = FaceAnalyzer()
