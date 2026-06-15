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
            "image": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=600&q=80"
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
        },
        {
            "id": 4,
            "name": "Pompadour",
            "confidence": 84,
            "description": "Volume on top suits oval proportions",
            "price": 300,
            "duration": "35 min",
            "tags": ["Trending"],
            "image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 5,
            "name": "Brush Up",
            "confidence": 80,
            "description": "Casual yet polished look",
            "price": 220,
            "duration": "25 min",
            "tags": ["Popular"],
            "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 6,
            "name": "Curly Fade",
            "confidence": 78,
            "description": "Natural curls with clean fade",
            "price": 260,
            "duration": "30 min",
            "tags": ["Natural"],
            "image": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=600&q=80"
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
            "image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=600&q=80"
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
            "image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 4,
            "name": "High Fade",
            "confidence": 85,
            "description": "Sharp fade adds definition",
            "price": 240,
            "duration": "30 min",
            "tags": ["Popular"],
            "image": "https://images.unsplash.com/photo-1596728325488-58c87691e9af?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 5,
            "name": "Textured Crop",
            "confidence": 81,
            "description": "Messy top with tight sides",
            "price": 210,
            "duration": "25 min",
            "tags": ["Modern"],
            "image": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 6,
            "name": "Slicked Back",
            "confidence": 77,
            "description": "Clean back elongates round face",
            "price": 230,
            "duration": "25 min",
            "tags": ["Classic"],
            "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=600&q=80"
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
            "image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 4,
            "name": "Pompadour",
            "confidence": 84,
            "description": "Volume on top balances wide jaw",
            "price": 290,
            "duration": "35 min",
            "tags": ["Trending"],
            "image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 5,
            "name": "Textured Spikes",
            "confidence": 79,
            "description": "Edgy look for strong features",
            "price": 230,
            "duration": "25 min",
            "tags": ["Bold"],
            "image": "https://images.unsplash.com/photo-1596728325488-58c87691e9af?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 6,
            "name": "Mid Fade",
            "confidence": 76,
            "description": "Clean mid fade complements jaw",
            "price": 210,
            "duration": "25 min",
            "tags": ["Modern"],
            "image": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=600&q=80"
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
        },
        {
            "id": 4,
            "name": "Medium Messy",
            "confidence": 82,
            "description": "Soft texture reduces forehead focus",
            "price": 240,
            "duration": "28 min",
            "tags": ["Modern"],
            "image": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 5,
            "name": "Pompadour",
            "confidence": 78,
            "description": "Volume balanced with wider forehead",
            "price": 290,
            "duration": "35 min",
            "tags": ["Trending"],
            "image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 6,
            "name": "Slick Out",
            "confidence": 75,
            "description": "Swept outwards balances proportions",
            "price": 220,
            "duration": "25 min",
            "tags": ["Classic"],
            "image": "https://images.unsplash.com/photo-1596728325488-58c87691e9af?auto=format&fit=crop&w=600&q=80"
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
            "image": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 4,
            "name": "Textured Crop",
            "confidence": 82,
            "description": "Adds width through texture",
            "price": 210,
            "duration": "25 min",
            "tags": ["Popular"],
            "image": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 5,
            "name": "Longer Fringe",
            "confidence": 77,
            "description": "Covers forehead to reduce length",
            "price": 230,
            "duration": "30 min",
            "tags": ["Modern"],
            "image": "https://images.unsplash.com/photo-1596728325488-58c87691e9af?auto=format&fit=crop&w=600&q=80"
        },
        {
            "id": 6,
            "name": "Classic Pompadour",
            "confidence": 74,
            "description": "Adds both height and width",
            "price": 300,
            "duration": "35 min",
            "tags": ["Classic"],
            "image": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?auto=format&fit=crop&w=600&q=80"
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
        },
        {
            "id": 3,
            "name": "Goatee",
            "confidence": 82,
            "description": "Defined chin accent",
            "price": 110,
            "duration": "15 min",
            "tags": ["Classic"]
        },
        {
            "id": 4,
            "name": "Full Beard",
            "confidence": 79,
            "description": "Bold and masculine look",
            "price": 150,
            "duration": "25 min",
            "tags": ["Bold"]
        },
        {
            "id": 5,
            "name": "Anchor Beard",
            "confidence": 75,
            "description": "Sharp, defined beard style",
            "price": 130,
            "duration": "20 min",
            "tags": ["Modern"]
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
        },
        {
            "id": 3,
            "name": "Chin Strap",
            "confidence": 83,
            "description": "Outlines jaw for definition",
            "price": 105,
            "duration": "15 min",
            "tags": ["Popular"]
        },
        {
            "id": 4,
            "name": "Short Stubble",
            "confidence": 80,
            "description": "Light beard adds angular lines",
            "price": 100,
            "duration": "15 min",
            "tags": ["Minimal"]
        },
        {
            "id": 5,
            "name": "Boxed Beard",
            "confidence": 76,
            "description": "Structured beard adds sharpness",
            "price": 140,
            "duration": "25 min",
            "tags": ["Modern"]
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
        },
        {
            "id": 3,
            "name": "Short Stubble",
            "confidence": 81,
            "description": "Rugged look for strong jaw",
            "price": 100,
            "duration": "15 min",
            "tags": ["Minimal"]
        },
        {
            "id": 4,
            "name": "Moustache",
            "confidence": 77,
            "description": "Classic solo moustache",
            "price": 80,
            "duration": "10 min",
            "tags": ["Classic"]
        },
        {
            "id": 5,
            "name": "Anchor Beard",
            "confidence": 73,
            "description": "Defined lines complement jaw",
            "price": 130,
            "duration": "20 min",
            "tags": ["Modern"]
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
        },
        {
            "id": 3,
            "name": "Short Stubble",
            "confidence": 80,
            "description": "Adds texture to lower face",
            "price": 100,
            "duration": "15 min",
            "tags": ["Minimal"]
        },
        {
            "id": 4,
            "name": "Goatee",
            "confidence": 76,
            "description": "Defines chin area",
            "price": 110,
            "duration": "15 min",
            "tags": ["Popular"]
        },
        {
            "id": 5,
            "name": "French Beard",
            "confidence": 72,
            "description": "Elegant narrow beard",
            "price": 120,
            "duration": "20 min",
            "tags": ["Classic"]
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
        },
        {
            "id": 3,
            "name": "Full Beard",
            "confidence": 85,
            "description": "Full beard adds face width",
            "price": 150,
            "duration": "25 min",
            "tags": ["Bold"]
        },
        {
            "id": 4,
            "name": "Short Stubble",
            "confidence": 78,
            "description": "Subtle width without bulk",
            "price": 100,
            "duration": "15 min",
            "tags": ["Minimal"]
        },
        {
            "id": 5,
            "name": "Van Dyke",
            "confidence": 74,
            "description": "Adds angular width to face",
            "price": 130,
            "duration": "20 min",
            "tags": ["Trending"]
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
        },
        {
            "id": 4,
            "name": "Platinum Blonde",
            "confidence": 82,
            "description": "Trendy bold blonde for fair skin",
            "colorCode": "#FAF0E6",
            "price": 1100,
            "duration": "80 min",
            "tags": ["Bold"]
        },
        {
            "id": 5,
            "name": "Rose Gold",
            "confidence": 77,
            "description": "Fashion-forward pinkish tone",
            "colorCode": "#E8A2B0",
            "price": 1200,
            "duration": "85 min",
            "tags": ["Trending"]
        },
        {
            "id": 6,
            "name": "Cool Brown",
            "confidence": 74,
            "description": "Subtle cool-toned brown",
            "colorCode": "#6B5B4F",
            "price": 780,
            "duration": "55 min",
            "tags": ["Natural"]
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
        },
        {
            "id": 4,
            "name": "Caramel",
            "confidence": 86,
            "description": "Golden caramel highlights medium skin",
            "colorCode": "#A67B5B",
            "price": 950,
            "duration": "70 min",
            "tags": ["Trending"]
        },
        {
            "id": 5,
            "name": "Burgundy",
            "confidence": 80,
            "description": "Rich red-brown for medium skin",
            "colorCode": "#6E0D25",
            "price": 1000,
            "duration": "75 min",
            "tags": ["Bold"]
        },
        {
            "id": 6,
            "name": "Honey Blonde",
            "confidence": 76,
            "description": "Warm honey shade for medium tone",
            "colorCode": "#D4A76A",
            "price": 1050,
            "duration": "75 min",
            "tags": ["Popular"]
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
        },
        {
            "id": 4,
            "name": "Blue Black",
            "confidence": 84,
            "description": "Cool blue tint for dark skin",
            "colorCode": "#0A0A2E",
            "price": 850,
            "duration": "60 min",
            "tags": ["Bold"]
        },
        {
            "id": 5,
            "name": "Warm Brown",
            "confidence": 79,
            "description": "Rich warm brown for dimension",
            "colorCode": "#4A2C1B",
            "price": 820,
            "duration": "60 min",
            "tags": ["Popular"]
        },
        {
            "id": 6,
            "name": "Copper",
            "confidence": 75,
            "description": "Vibrant copper for dark complexion",
            "colorCode": "#8B4513",
            "price": 980,
            "duration": "70 min",
            "tags": ["Trending"]
        }
    ]
}

# Default fallback
DEFAULT_FACE_SHAPE = "oval"
DEFAULT_SKIN_TONE = "medium"