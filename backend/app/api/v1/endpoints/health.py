"""
Health Check Endpoint
System health and status monitoring
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns system status and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "AuthBrasil CNPJ API",
        "version": "0.1.0",
    }


@router.get("/health/detailed")
async def detailed_health_check():
    """
    Detailed health check
    Includes database and cache status (to be implemented)
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "AuthBrasil CNPJ API",
        "version": "0.1.0",
        "components": {
            "api": "operational",
            "database": "not_configured",  # Will be updated when DB is ready
            "cache": "not_configured",     # Will be updated when Redis is ready
        }
    }
