import threading
from utils.constants import (
    FACE_SHAPE_HAIRCUTS,
    FACE_SHAPE_BEARDS,
    SKIN_TONE_COLORS,
    DEFAULT_FACE_SHAPE,
    DEFAULT_SKIN_TONE,
)
from services.wiki_fetcher import get_wiki_hairstyles, get_wiki_beards


class StyleRecommender:
    _wiki_hair = None
    _wiki_beards = None
    _wiki_lock = threading.Lock()

    def _load_wiki_haircuts(self) -> list:
        with self._wiki_lock:
            if self._wiki_hair is None:
                try:
                    self._wiki_hair = get_wiki_hairstyles()
                except Exception as e:
                    print(f"[Recommender] Wiki haircuts failed: {e}")
                    self._wiki_hair = []
            return self._wiki_hair or []

    def _load_wiki_beards(self) -> list:
        with self._wiki_lock:
            if self._wiki_beards is None:
                try:
                    self._wiki_beards = get_wiki_beards()
                except Exception as e:
                    print(f"[Recommender] Wiki beards failed: {e}")
                    self._wiki_beards = []
            return self._wiki_beards or []

    def _adjust_confidence(self, base_confidence: int, shape_confidence: int, adjustments: list) -> int:
        score = base_confidence
        score = int(score * (shape_confidence / 100))
        for adj in adjustments:
            score += adj
        return max(10, min(98, score))

    def _get_reason(self, shape: str, features: dict, item_name: str) -> str:
        reasons = []
        jaw = (features or {}).get("jaw_type", "")
        forehead = (features or {}).get("forehead_type", "")
        cheeks = (features or {}).get("cheek_type", "")
        chin = (features or {}).get("chin_type", "")
        balance = (features or {}).get("face_balance", 0)

        shape_reasons = {
            "Oval": (["Most styles suit oval faces", "Balanced proportions"]),
            "Round": (["Adds vertical definition", "Creates angular contrast"]),
            "Square": (["Softens strong jawline", "Adds height to balance"]),
            "Heart": (["Balances wider forehead", "Adds width to lower face"]),
            "Oblong": (["Adds width to long face", "Reduces face length visually"]),
            "Diamond": (["Highlights cheekbones", "Balances narrow features"]),
            "Triangle": (["Balances narrow forehead", "Softens wide jawline"]),
        }

        reason_list = list(shape_reasons.get(shape, ("Personalized for your face",)))

        if "points" in item_name.lower() or "taper" in item_name.lower():
            if "Square" in jaw or "Strong" in jaw:
                reasons.append("Complements strong jawline")
            if "Narrow" in chin:
                reasons.append("Adds fullness to lower face")

        if "fringe" in item_name.lower() or "bangs" in item_name.lower():
            if "Wide" in forehead:
                reasons.append("Softens forehead width")
            if "Narrow" in forehead:
                reasons.append("Adds volume to upper face")

        if "volume" in item_name.lower() or "pompadour" in item_name.lower() or "quiff" in item_name.lower():
            if balance and balance > 1.3:
                reasons.append("Adds width to elongated face")
            if "Narrow" in forehead:
                reasons.append("Creates fullness on top")

        if "side" in item_name.lower() or "swept" in item_name.lower():
            if "Heart" in shape:
                reasons.append("Redirects attention from forehead")
            if "Round" in shape:
                reasons.append("Creates asymmetrical interest")

        if "buzz" in item_name.lower() or "crew" in item_name.lower() or "short" in item_name.lower():
            if "Strong" in jaw:
                reasons.append("Highlights facial structure")
            if "Square" in shape:
                reasons.append("Clean, sharp appearance")

        all_reasons = list(reason_list) + reasons
        return all_reasons[0] if all_reasons else "Personalized for you"

    def get_haircut_recommendations(self, face_shape: str, shape_confidence: int = 80,
                                     features: dict = None) -> list:
        wiki_hair = self._load_wiki_haircuts()

        if wiki_hair:
            hair = sorted(wiki_hair, key=lambda x: x["confidence"], reverse=True)
            result = []
            for item in hair:
                adj_conf = self._adjust_confidence(item["confidence"], shape_confidence, [0])
                reason = self._get_reason(face_shape, features, item["name"])
                result.append({
                    "id": item["id"],
                    "name": item["name"],
                    "confidence": adj_conf,
                    "description": reason,
                    "price": item["price"],
                    "duration": item["duration"],
                    "tags": item["tags"],
                    "image": item.get("image"),
                })
            return result

        shape_key = face_shape.lower()
        haircuts = FACE_SHAPE_HAIRCUTS.get(shape_key, FACE_SHAPE_HAIRCUTS[DEFAULT_FACE_SHAPE])
        haircuts = sorted(haircuts, key=lambda x: x["confidence"], reverse=True)

        result = []
        for item in haircuts:
            adj_conf = self._adjust_confidence(item["confidence"], shape_confidence, [0])
            reason = self._get_reason(face_shape, features, item["name"])
            result.append({
                "id": item["id"],
                "name": item["name"],
                "confidence": adj_conf,
                "description": reason,
                "price": item["price"],
                "duration": item["duration"],
                "tags": item["tags"],
                "image": item.get("image"),
            })
        return result

    def get_beard_recommendations(self, face_shape: str, shape_confidence: int = 80,
                                   features: dict = None) -> list:
        wiki_beards = self._load_wiki_beards()

        if wiki_beards:
            beards = sorted(wiki_beards, key=lambda x: x["confidence"], reverse=True)
            result = []
            for item in beards:
                adj_conf = self._adjust_confidence(item["confidence"], shape_confidence, [0])
                result.append({
                    "id": item["id"],
                    "name": item["name"],
                    "confidence": adj_conf,
                    "description": item.get("description", "Style from Wikipedia").capitalize(),
                    "price": item["price"],
                    "duration": item["duration"],
                    "tags": item["tags"],
                    "image": item.get("image"),
                })
            return result

        shape_key = face_shape.lower()
        beards = FACE_SHAPE_BEARDS.get(shape_key, FACE_SHAPE_BEARDS[DEFAULT_FACE_SHAPE])
        beards = sorted(beards, key=lambda x: x["confidence"], reverse=True)

        result = []
        for item in beards:
            adj_conf = self._adjust_confidence(item["confidence"], shape_confidence, [0])
            result.append({
                "id": item["id"],
                "name": item["name"],
                "confidence": adj_conf,
                "description": item.get("description", "Matches your face shape").capitalize(),
                "price": item["price"],
                "duration": item["duration"],
                "tags": item["tags"],
                "image": item.get("image"),
            })
        return result

    def get_color_recommendations(self, skin_tone: str, tone_confidence: int = 80,
                                   undertone: str = "Neutral") -> list:
        tone_key = skin_tone.lower()
        colors = SKIN_TONE_COLORS.get(tone_key, SKIN_TONE_COLORS[DEFAULT_SKIN_TONE])
        colors = sorted(colors, key=lambda x: x["confidence"], reverse=True)

        result = []
        for item in colors:
            adj_conf = self._adjust_confidence(item["confidence"], tone_confidence,
                                                [5 if "neutral" in undertone.lower() else 0])

            reason = f"Perfect match for {skin_tone.lower()} skin tone"
            if undertone and undertone.lower() != "neutral":
                if "cool" in item["name"].lower() and "cool" in undertone.lower():
                    adj_conf = min(98, adj_conf + 5)
                    reason = f"Cool undertone ({undertone.lower()}) enhances this shade"
                elif "warm" in item["name"].lower() and "warm" in undertone.lower():
                    adj_conf = min(98, adj_conf + 5)
                    reason = f"Warm undertone ({undertone.lower()}) complements this shade"

            result.append({
                "id": item["id"],
                "name": item["name"],
                "confidence": adj_conf,
                "description": reason,
                "colorCode": item["colorCode"],
                "price": item["price"],
                "duration": item["duration"],
                "tags": item["tags"],
                "image": item.get("image"),
            })
        return result

    def get_user_recommendations(self, user_id: str, booking_history: list = None) -> dict:
        """User history ke basis par personalized recommendations"""
        return {
            "user_id": user_id,
            "recommendations": [
                {
                    "id": 1,
                    "name": "Classic Undercut",
                    "confidence": 92,
                    "description": "Perfect for your face shape",
                    "price": 250,
                    "duration": "30 min",
                    "tags": ["Best Match", "Trending"],
                    "image": "https://images.unsplash.com/photo-1596728325488-58c87691e9af?auto=format&fit=crop&w=600&q=80"
                },
                {
                    "id": 2,
                    "name": "Textured Crop",
                    "confidence": 85,
                    "description": "Modern and stylish choice",
                    "price": 200,
                    "duration": "25 min",
                    "tags": ["Popular"],
                    "image": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=600&q=80"
                },
                {
                    "id": 3,
                    "name": "Pompadour",
                    "confidence": 78,
                    "description": "Classic volume on top",
                    "price": 280,
                    "duration": "35 min",
                    "tags": ["Classic"],
                    "image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=600&q=80"
                }
            ]
        }

    def get_trending(self, city: str = "default") -> list:
        """City ke trending services — market se popular styles"""
        return [
            {"name": "Textured Crop", "count": 142, "trending": True},
            {"name": "Skin Fade", "count": 131, "trending": True},
            {"name": "Pompadour", "count": 119, "trending": True},
            {"name": "Crew Cut", "count": 98, "trending": True},
            {"name": "Mid Fade", "count": 87, "trending": True},
            {"name": "Side Part", "count": 76, "trending": False},
            {"name": "Buzz Cut", "count": 68, "trending": False},
            {"name": "French Crop", "count": 62, "trending": False},
            {"name": "Slick Back", "count": 55, "trending": False},
            {"name": "Quiff", "count": 51, "trending": False},
            {"name": "Ivy League", "count": 47, "trending": False},
            {"name": "Faux Hawk", "count": 43, "trending": False},
        ]


# Singleton
recommender = StyleRecommender()
