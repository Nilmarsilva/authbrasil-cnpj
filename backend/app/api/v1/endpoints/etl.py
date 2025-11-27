"""
ETL Endpoints
Admin-only endpoints for managing ETL jobs
"""

import os
import asyncio
import logging
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.db.session import get_async_db
from app.models.user import User
from app.models.etl_status import ETLStatus
from app.core.deps import get_current_superuser
from app.schemas.etl import (
    ETLStartRequest,
    ETLStartResponse,
    ETLStatusResponse,
    ETLValidationResponse,
    ETLLogsResponse
)
from app.etl.worker_v2 import ETLWorker

router = APIRouter()
logger = logging.getLogger(__name__)

# Global ETL task reference
current_etl_task = None


def get_disk_space():
    """Get disk space in GB"""
    stat = os.statvfs('/')
    free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
    used_gb = ((stat.f_blocks - stat.f_bfree) * stat.f_frsize) / (1024**3)
    return free_gb, used_gb


def check_postgres_running() -> bool:
    """Check if PostgreSQL container is running"""
    try:
        import subprocess
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=postgres", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return "postgres" in result.stdout.lower()
    except Exception:
        return False


async def check_tables_exist(db: AsyncSession) -> bool:
    """Check if required tables exist"""
    try:
        # Simple check - try to count empresas
        result = await db.execute("SELECT COUNT(*) FROM empresas LIMIT 1")
        return True
    except Exception:
        return False


@router.get("/validate", response_model=ETLValidationResponse)
async def validate_etl(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Validate ETL pre-conditions
    Admin only
    """
    warnings = []
    errors = []
    
    # Check disk space
    free_gb, used_gb = get_disk_space()
    
    if free_gb < 30:
        warnings.append(f"⚠️ Apenas {free_gb:.1f}GB livres. Recomendado: 40GB+")
    
    if free_gb < 15:
        errors.append(f"❌ Espaço crítico: {free_gb:.1f}GB. Mínimo: 15GB")
    
    # Check PostgreSQL
    postgres_running = check_postgres_running()
    if not postgres_running:
        errors.append("❌ PostgreSQL não está rodando")
    
    # Check tables
    tables_exist = await check_tables_exist(db)
    if not tables_exist:
        errors.append("❌ Tabelas não existem. Execute migrations primeiro")
    
    return {
        "can_proceed": len(errors) == 0,
        "warnings": warnings,
        "errors": errors,
        "disk_free_gb": free_gb,
        "disk_used_gb": used_gb,
        "postgres_running": postgres_running,
        "tables_exist": tables_exist
    }


async def run_etl_worker(job_id: str, skip_download: bool, tables: List[str]):
    """Background task to run ETL worker"""
    global current_etl_task
    try:
        worker = ETLWorker(job_id=job_id, skip_download=skip_download, tables=tables)
        await worker.run()
    except Exception as e:
        logger.error(f"ETL worker failed: {e}", exc_info=True)
    finally:
        current_etl_task = None


@router.post("/start", response_model=ETLStartResponse)
async def start_etl(
    request: ETLStartRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Start ETL job
    Admin only
    """
    global current_etl_task
    
    # Check if already running
    if current_etl_task is not None and not current_etl_task.done():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="ETL job já está em execução"
        )
    
    # Validate
    if not request.force:
        free_gb, used_gb = get_disk_space()
        if free_gb < 15:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Espaço insuficiente: {free_gb:.1f}GB. Use force=true para ignorar."
            )
    
    # Create new ETL status
    job_id = f"etl_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    
    etl_status = ETLStatus(
        job_id=job_id,
        status="idle",
        progress_percent=0.0,
        files_processed=0,
        files_total=0,
        records_imported=0
    )
    
    db.add(etl_status)
    await db.commit()
    await db.refresh(etl_status)
    
    # Start background task
    current_etl_task = asyncio.create_task(
        run_etl_worker(job_id, request.skip_download, request.tables)
    )
    
    logger.info(f"ETL job {job_id} started by {current_user.email}")
    
    return {
        "status": "started",
        "job_id": job_id,
        "message": "ETL iniciado com sucesso"
    }


@router.get("/status", response_model=ETLStatusResponse)
async def get_etl_status(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Get current ETL status
    Admin only
    """
    # Get latest ETL status
    result = await db.execute(
        select(ETLStatus).order_by(desc(ETLStatus.created_at)).limit(1)
    )
    etl_status = result.scalar_one_or_none()
    
    if not etl_status:
        # No ETL ever run, return idle
        return ETLStatusResponse(
            job_id="none",
            status="idle",
            progress_percent=0.0,
            files_processed=0,
            files_total=0,
            records_imported=0
        )
    
    return ETLStatusResponse.from_orm(etl_status)


@router.get("/logs", response_model=ETLLogsResponse)
async def get_etl_logs(
    lines: int = 100,
    current_user: User = Depends(get_current_superuser)
):
    """
    Get ETL logs
    Admin only
    """
    import subprocess
    
    try:
        # Try to read from log file
        result = subprocess.run(
            ["tail", "-n", str(lines), "/var/log/etl.log"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            log_lines = result.stdout.strip().split('\n')
            return {
                "logs": log_lines,
                "total_lines": len(log_lines)
            }
    except Exception:
        pass
    
    # Fallback: empty logs
    return {
        "logs": ["Logs não disponíveis"],
        "total_lines": 0
    }


@router.post("/pause")
async def pause_etl(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Pause ETL job
    Admin only
    (Not fully implemented - requires worker cooperation)
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Pause not implemented yet"
    )


@router.post("/resume")
async def resume_etl(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_superuser)
):
    """
    Resume ETL job
    Admin only
    (Not fully implemented - requires worker state persistence)
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Resume not implemented yet"
    )
