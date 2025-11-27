"""
API v1 Router
Aggregates all API endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health, cnpj, auth, cnpj_insights, etl

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(cnpj.router, prefix="/cnpj", tags=["cnpj"])
api_router.include_router(cnpj_insights.router, prefix="/insights", tags=["insights"])
api_router.include_router(etl.router, prefix="/etl", tags=["etl"])
