"""
Health Check Endpoints
Tests API and Redis connectivity
"""
from fastapi import APIRouter, HTTPException
from redis import Redis
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Basic health check endpoint
    Returns API status and Redis connectivity
    """
    redis_status = "disconnected"
    redis_error = None
    
    try:
        # Test Redis connection
        redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
        redis_client.ping()
        redis_status = "connected"
        redis_client.close()
    except Exception as e:
        redis_error = str(e)
    
    return {
        "status": "healthy" if redis_status == "connected" else "degraded",
        "api": "running",
        "redis": redis_status,
        "redis_error": redis_error,
        "environment": settings.app_env,
        "llm_provider": settings.llm_provider
    }

