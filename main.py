# silverscisor-python/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from routers import analysis, recommendations, payment, service_requests, generation

load_dotenv()

app = FastAPI(
    title="Silverscisor AI Service",
    description="Face analysis and style recommendation service",
    version="1.0.0"
)

# CORS middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers include karo
app.include_router(analysis.router)
app.include_router(recommendations.router)
app.include_router(payment.router)
app.include_router(service_requests.router)
app.include_router(generation.router)


@app.get("/")
async def root():
    return {
        "service": "Silverscisor AI Service",
        "status": "Running",
        "endpoints": [
            "POST /api/analyze-face",
            "POST /api/create-order",
            "POST /api/verify-payment",
            "GET /api/recommendations/user/{user_id}",
            "GET /api/recommendations/trending",
            "GET /api/health",
            "POST /api/service-requests",
            "GET /api/service-requests",
            "GET /api/service-requests/{id}",
            "POST /api/service-requests/{id}/accept",
            "POST /api/service-requests/{id}/schedule",
            "POST /api/service-requests/{id}/cancel",
            "POST /api/generate-style-images"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5004))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)