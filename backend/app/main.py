"""
Prompt Wars - FastAPI Backend Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import health, websockets, redis_test, cards

app = FastAPI(
    title="Prompt Wars API",
    description="AI-Powered Text-Based Strategy Game",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(websockets.router, tags=["websockets"])
app.include_router(redis_test.router, prefix="/api", tags=["redis"])
app.include_router(cards.router, prefix="/api", tags=["cards"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Prompt Wars API",
        "version": "1.0.0",
        "docs": "/docs"
    }

