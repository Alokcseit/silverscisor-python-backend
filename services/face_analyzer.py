import os
import math
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SHAPE_PROFILES = {
    "Oval":     [1.35, 0.92, 0.82, 1.12],
    "Round":    [1.10, 0.95, 0.88, 1.08],
    "Square":   [1.20, 0.92, 0.90, 1.02],
    "Heart":    [1.30, 0.98, 0.75, 1.30],
    "Oblong":   [1.55, 0.88, 0.80, 1.10],
    "Diamond":  [1.40, 0.85, 0.75, 1.13],
    "Triangle": [1.25, 0.85, 0.95, 0.89],
}

RATIO_WEIGHTS = [0.35, 0.20, 0.25, 0.20]


class FaceAnalyzer:
    def __init__(self):
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        if self.face_cascade.empty():
            print("[FaceAnalyzer] Failed to load Haar cascade")

    def detect_face(self, img_rgb: np.ndarray) -> bool:
        gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))
        return len(faces) > 0

    def _get_face_width_profile(self, gray_roi):
        h, w = gray_roi.shape
        if h < 20 or w < 20:
            return {}

        blurred = cv2.GaussianBlur(gray_roi, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return {}

        contour = max(contours, key=cv2.contourArea)
        pts = contour[:, 0, :]

        widths = {}
        for pct in [0.10, 0.25, 0.30, 0.40, 0.50, 0.55, 0.60, 0.70, 0.75, 0.80, 0.85, 0.90]:
            y_line = int(h * pct)
            mask = np.abs(pts[:, 1] - y_line) < 3
            line_pts = pts[mask]
            if len(line_pts) > 1:
                widths[pct] = (int(line_pts[:, 0].min()), int(line_pts[:, 0].max()))
            else:
                widths[pct] = (0, w)

        return widths

    def get_landmarks(self, img_rgb: np.ndarray):
        gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))
        if len(faces) == 0:
            return None

        x, y, w, h = faces[0]

        forehead_margin = int(h * 0.2)
        y = max(0, y - forehead_margin)
        h = min(gray.shape[0] - y, h + forehead_margin)

        face_roi = gray[y:y+h, x:x+w]
        widths = self._get_face_width_profile(face_roi)

        cx = x + w // 2

        def _w(pct):
            l, r = widths.get(pct, (0, w))
            return x + l, x + r

        fw20_l, fw20_r = _w(0.20)
        fw50_l, fw50_r = _w(0.50)
        fw75_l, fw75_r = _w(0.75)
        fw90_l, fw90_r = _w(0.90)

        landmarks = {
            "forehead_top":       (cx, y),
            "chin_bottom":        (cx, y + h),
            "left_temple":        (fw20_l, y + int(h * 0.20)),
            "right_temple":       (fw20_r, y + int(h * 0.20)),
            "left_cheek":         (fw50_l, y + int(h * 0.50)),
            "right_cheek":        (fw50_r, y + int(h * 0.50)),
            "left_jaw":           (fw75_l, y + int(h * 0.75)),
            "right_jaw":          (fw75_r, y + int(h * 0.75)),
            "chin_left":          (fw90_l, y + int(h * 0.90)),
            "chin_right":         (fw90_r, y + int(h * 0.90)),
            "nose_bridge_top":    (cx, y + int(h * 0.42)),
            "nose_bridge_bottom": (cx, y + int(h * 0.52)),
            "left_eye_outer":     (x + int(w * 0.22), y + int(h * 0.33)),
            "right_eye_outer":    (x + int(w * 0.78), y + int(h * 0.33)),
        }

        return landmarks

    def _distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def extract_face_measurements(self, landmarks):
        pts = landmarks
        face_length = self._distance(pts["forehead_top"], pts["chin_bottom"])
        forehead_width = self._distance(pts["left_temple"], pts["right_temple"])
        cheek_width = self._distance(pts["left_cheek"], pts["right_cheek"])
        jaw_width = self._distance(pts["left_jaw"], pts["right_jaw"])
        chin_width = self._distance(pts["chin_left"], pts["chin_right"])

        ratios = {
            "length_width": face_length / cheek_width if cheek_width else 1,
            "forehead_cheek": forehead_width / cheek_width if cheek_width else 1,
            "jaw_cheek": jaw_width / cheek_width if cheek_width else 1,
            "forehead_jaw": forehead_width / jaw_width if jaw_width else 1,
            "jaw_forehead": jaw_width / forehead_width if forehead_width else 1,
            "chin_cheek": chin_width / cheek_width if cheek_width else 1,
        }

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

    def calculate_face_shape(self, landmarks: dict) -> dict:
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

    def get_hair_length_estimate(self, landmarks: dict, img_height: int) -> tuple:
        try:
            forehead_top = landmarks["forehead_top"]
            chin = landmarks["chin_bottom"]
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
        except KeyError:
            return "Short", 50

    def analyze(self, img_rgb: np.ndarray) -> dict:
        h, w = img_rgb.shape[:2]

        has_face = self.detect_face(img_rgb)
        if not has_face:
            print("[FaceAnalyzer] No face detected in image")
            return {"success": False, "error": "No face detected"}

        landmarks = self.get_landmarks(img_rgb)
        if landmarks is None:
            print("[FaceAnalyzer] Could not compute facial landmarks")
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


face_analyzer = FaceAnalyzer()
