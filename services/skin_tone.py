import cv2
import numpy as np


class SkinToneAnalyzer:
    def __init__(self):
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def analyze_skin_tone(self, img_rgb: np.ndarray) -> dict:
        try:
            gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))
            if len(faces) == 0:
                print("[SkinTone] No face detected")
                return {"tone": "Medium", "confidence": 50, "details": "No face detected"}

            x, y, w, h = faces[0]

            regions = {
                "left_cheek":  (y + int(h*0.40), y + int(h*0.70), x + int(w*0.05), x + int(w*0.30)),
                "right_cheek": (y + int(h*0.40), y + int(h*0.70), x + int(w*0.70), x + int(w*0.95)),
                "forehead":    (y + int(h*0.05), y + int(h*0.30), x + int(w*0.20), x + int(w*0.80)),
                "nose":        (y + int(h*0.42), y + int(h*0.60), x + int(w*0.35), x + int(w*0.65)),
            }

            all_pixels = []
            for y1, y2, x1, x2 in regions.values():
                if y2 > y1 and x2 > x1:
                    region = img_rgb[y1:y2, x1:x2]
                    if region.size > 0:
                        all_pixels.append(region)

            if not all_pixels:
                print("[SkinTone] No skin regions found")
                return {"tone": "Medium", "confidence": 50, "details": "No skin regions found"}

            combined = np.concatenate([p.reshape(-1, 3) for p in all_pixels], axis=0)
            pixels_uint8 = combined.astype(np.uint8)

            ycrcb = cv2.cvtColor(pixels_uint8.reshape(1, -1, 3), cv2.COLOR_RGB2YCrCb)
            avg_y = float(np.mean(ycrcb[0, :, 0]))

            hsv = cv2.cvtColor(pixels_uint8.reshape(1, -1, 3), cv2.COLOR_RGB2HSV)
            avg_h = float(np.mean(hsv[0, :, 0]))
            avg_s = float(np.mean(hsv[0, :, 1]))
            avg_v = float(np.mean(hsv[0, :, 2]))

            lab = cv2.cvtColor(pixels_uint8.reshape(1, -1, 3), cv2.COLOR_RGB2Lab)
            avg_l = float(np.mean(lab[0, :, 0]))
            avg_a = float(np.mean(lab[0, :, 1]))
            avg_b_val = float(np.mean(lab[0, :, 2]))

            brightness_score = avg_y * 0.5 + avg_l * 0.5

            tone = "Medium"
            confidence = 60
            undertone = "Neutral"

            if avg_a > 14:
                undertone = "Warm"
            elif avg_a < 10:
                undertone = "Cool"
            else:
                undertone = "Neutral"

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

            if avg_s > 50:
                tone_quality = "Rich"
            elif avg_s > 30:
                tone_quality = "Natural"
            else:
                tone_quality = "Subtle"

            details = f"{tone_quality} {tone} tone with {undertone.lower()} undertone"

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


skin_analyzer = SkinToneAnalyzer()
