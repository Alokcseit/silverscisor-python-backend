# silverscisor-python/utils/constants.py

# Face Shape → Hairstyle Mapping
FACE_SHAPE_HAIRCUTS = {
    "oval": [
        {
            "id": 1,
            "name": "Classic Undercut",
            "confidence": 95,
            "description": "Perfect for oval face - most styles work well",
            "price": 250,
            "duration": "30 min",
            "tags": ["Best Match", "Trending"],
            "image": "https://images.unsplash.com/photo-1596728325488-58c87691e9af?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 2,
            "name": "Textured Crop",
            "confidence": 88,
            "description": "Modern and stylish for oval faces",
            "price": 200,
            "duration": "25 min",
            "tags": ["Popular"],
            "image": "https://images.unsplash.com/photo-1567894340315-735d7c361db7?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 3,
            "name": "Side Part",
            "confidence": 82,
            "description": "Classic professional look",
            "price": 180,
            "duration": "20 min",
            "tags": ["Classic"],
            "image": "https://images.unsplash.com/photo-1596728325488-58c87691e9af?auto=format&fit=crop&w=600&q=80"
        }
    ],
    "round": [
        {
            "id": 1,
            "name": "Pompadour",
            "confidence": 94,
            "description": "Adds height, slims round face",
            "price": 280,
            "duration": "35 min",
            "tags": ["Best Match", "Trending"],
            "image": "https://images.unsplash.com/photo-1525875975471-9a1b542561e8?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 2,
            "name": "Quiff",
            "confidence": 89,
            "description": "Volume on top elongates face",
            "price": 260,
            "duration": "30 min",
            "tags": ["Popular"],
            "image": "https://images.unsplash.com/photo-1596728325488-58c87691e9af?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 3,
            "name": "Faux Hawk",
            "confidence": 83,
            "description": "Creates angular look for round face",
            "price": 220,
            "duration": "25 min",
            "tags": ["Bold"],
            "image": "https://images.unsplash.com/photo-1525875975471-9a1b542561e8?auto=format&fit=crop&w=600&q=80"
        }
    ],
    "square": [
        {
            "id": 1,
            "name": "Crew Cut",
            "confidence": 93,
            "description": "Clean cut suits strong jawline",
            "price": 180,
            "duration": "20 min",
            "tags": ["Best Match"],
            "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 2,
            "name": "Ivy League",
            "confidence": 87,
            "description": "Softens square features",
            "price": 200,
            "duration": "25 min",
            "tags": ["Classic"],
            "image": "https://images.unsplash.com/photo-1596728325488-58c87691e9af?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 3,
            "name": "Slick Back",
            "confidence": 81,
            "description": "Highlights strong facial structure",
            "price": 220,
            "duration": "25 min",
            "tags": ["Bold"],
            "image": "https://images.unsplash.com/photo-1525875975471-9a1b542561e8?auto=format&fit=crop&w=600&q=80"
        }
    ],
    "heart": [
        {
            "id": 1,
            "name": "Side Swept",
            "confidence": 92,
            "description": "Balances wider forehead",
            "price": 210,
            "duration": "25 min",
            "tags": ["Best Match"],
            "image": "https://images.unsplash.com/photo-1596728325488-58c87691e9af?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 2,
            "name": "Textured Fringe",
            "confidence": 86,
            "description": "Draws attention away from forehead",
            "price": 230,
            "duration": "30 min",
            "tags": ["Popular"],
            "image": "https://images.unsplash.com/photo-1596728325488-58c87691e9af?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 3,
            "name": "Caesar Cut",
            "confidence": 80,
            "description": "Balances proportions for heart face",
            "price": 190,
            "duration": "20 min",
            "tags": ["Classic"],
            "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=600&q=80"
        }
    ],
    "oblong": [
        {
            "id": 1,
            "name": "Fringe with Volume",
            "confidence": 91,
            "description": "Adds width to elongated face",
            "price": 240,
            "duration": "30 min",
            "tags": ["Best Match"],
            "image": "https://images.unsplash.com/photo-1596728325488-58c87691e9af?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 2,
            "name": "Buzz Cut with Taper",
            "confidence": 85,
            "description": "Keeps proportions balanced",
            "price": 160,
            "duration": "20 min",
            "tags": ["Popular"],
            "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 3,
            "name": "Curly Top",
            "confidence": 79,
            "description": "Natural volume reduces length",
            "price": 270,
            "duration": "35 min",
            "tags": ["Natural"],
            "image": "https://images.unsplash.com/photo-1567894340315-735d7c361db7?auto=format&fit=crop&w=600&q=80"
        }
    ]
}

# Face Shape → Beard Style Mapping
FACE_SHAPE_BEARDS = {
    "oval": [
        {
            "id": 1,
            "name": "Short Stubble",
            "confidence": 92,
            "description": "Works perfectly with oval face",
            "price": 100,
            "duration": "15 min",
            "tags": ["Best Match"]
        },
        {
            "id": 2,
            "name": "French Beard",
            "confidence": 86,
            "description": "Elegant and sophisticated",
            "price": 120,
            "duration": "20 min",
            "tags": ["Trending"]
        }
    ],
    "round": [
        {
            "id": 1,
            "name": "Goatee",
            "confidence": 93,
            "description": "Elongates round face visually",
            "price": 110,
            "duration": "15 min",
            "tags": ["Best Match"]
        },
        {
            "id": 2,
            "name": "Van Dyke",
            "confidence": 87,
            "description": "Sharp lines slim the face",
            "price": 130,
            "duration": "20 min",
            "tags": ["Classic"]
        }
    ],
    "square": [
        {
            "id": 1,
            "name": "Full Beard",
            "confidence": 90,
            "description": "Softens sharp jawline beautifully",
            "price": 140,
            "duration": "25 min",
            "tags": ["Best Match"]
        },
        {
            "id": 2,
            "name": "Circle Beard",
            "confidence": 84,
            "description": "Rounds the angular features",
            "price": 115,
            "duration": "20 min",
            "tags": ["Popular"]
        }
    ],
    "heart": [
        {
            "id": 1,
            "name": "Chin Strap",
            "confidence": 89,
            "description": "Adds width to narrow chin",
            "price": 105,
            "duration": "15 min",
            "tags": ["Best Match"]
        },
        {
            "id": 2,
            "name": "Mutton Chops",
            "confidence": 82,
            "description": "Balances wider forehead",
            "price": 125,
            "duration": "20 min",
            "tags": ["Bold"]
        }
    ],
    "oblong": [
        {
            "id": 1,
            "name": "Boxed Beard",
            "confidence": 91,
            "description": "Adds width to elongated face",
            "price": 135,
            "duration": "20 min",
            "tags": ["Best Match"]
        },
        {
            "id": 2,
            "name": "Handlebar Moustache",
            "confidence": 83,
            "description": "Creates width at mid-face",
            "price": 100,
            "duration": "15 min",
            "tags": ["Classic"]
        }
    ]
}

# Skin Tone → Hair Color Mapping
SKIN_TONE_COLORS = {
    "fair": [
        {
            "id": 1,
            "name": "Ash Brown",
            "confidence": 91,
            "description": "Cool tone complements fair skin",
            "colorCode": "#8B7355",
            "price": 800,
            "duration": "60 min",
            "tags": ["Best Match"]
        },
        {
            "id": 2,
            "name": "Golden Blonde",
            "confidence": 85,
            "description": "Warm blonde for fair complexion",
            "colorCode": "#F5DEB3",
            "price": 900,
            "duration": "70 min",
            "tags": ["Trending"]
        },
        {
            "id": 3,
            "name": "Natural Black",
            "confidence": 79,
            "description": "Classic contrast with fair skin",
            "colorCode": "#1A1A1A",
            "price": 700,
            "duration": "50 min",
            "tags": ["Classic"]
        }
    ],
    "medium": [
        {
            "id": 1,
            "name": "Dark Brown",
            "confidence": 93,
            "description": "Perfect complement for medium skin",
            "colorCode": "#3B1F0A",
            "price": 800,
            "duration": "60 min",
            "tags": ["Best Match"]
        },
        {
            "id": 2,
            "name": "Chestnut",
            "confidence": 88,
            "description": "Warm chestnut suits medium tone",
            "colorCode": "#954535",
            "price": 850,
            "duration": "65 min",
            "tags": ["Popular"]
        },
        {
            "id": 3,
            "name": "Warm Black",
            "confidence": 82,
            "description": "Rich black with warm undertones",
            "colorCode": "#1C1008",
            "price": 720,
            "duration": "55 min",
            "tags": ["Classic"]
        }
    ],
    "dark": [
        {
            "id": 1,
            "name": "Natural Black",
            "confidence": 95,
            "description": "Matches and enhances dark complexion",
            "colorCode": "#1A1A1A",
            "price": 700,
            "duration": "50 min",
            "tags": ["Best Match"]
        },
        {
            "id": 2,
            "name": "Dark Auburn",
            "confidence": 87,
            "description": "Rich auburn complements dark skin",
            "colorCode": "#6B2D0F",
            "price": 820,
            "duration": "60 min",
            "tags": ["Trending"]
        },
        {
            "id": 3,
            "name": "Soft Black",
            "confidence": 81,
            "description": "Slightly lightened for dimension",
            "colorCode": "#2D2D2D",
            "price": 750,
            "duration": "55 min",
            "tags": ["Natural"]
        }
    ]
}

# Default fallback
DEFAULT_FACE_SHAPE = "oval"
DEFAULT_SKIN_TONE = "medium"