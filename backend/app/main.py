"""
AuthBrasil CNPJ - Main Application
FastAPI application initialization and configuration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    print(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"Environment: {settings.ENVIRONMENT}")
    
    yield
    
    # Shutdown
    print(f"Shutting down {settings.PROJECT_NAME}")


# OpenAPI tags metadata
tags_metadata = [
    {
        "name": "health",
        "description": "Health check e status da API",
    },
    {
        "name": "cnpj",
        "description": "Consultas de CNPJ e dados corporativos",
    },
    {
        "name": "auth",
        "description": "Autenticação e gerenciamento de tokens",
    },
    {
        "name": "user",
        "description": "Gerenciamento de usuários e perfis",
    },
]

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=tags_metadata,
    contact={
        "name": "AuthBrasil Suporte",
        "email": "suporte@authbrasil.com.br",
        "url": "https://authbrasil.app.br",
    },
    license_info={
        "name": "Proprietary",
        "url": "https://authbrasil.app.br/termos",
    },
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": f"{settings.API_V1_STR}/docs",
    }
