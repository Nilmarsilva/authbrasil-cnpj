"""
ETL Schemas
Pydantic models for ETL API requests/responses
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class ETLStartRequest(BaseModel):
    """Request to start ETL job"""
    force: bool = Field(default=False, description="Ignorar avisos de espaço em disco")
    skip_download: bool = Field(default=False, description="Usar ZIPs já baixados (se disponíveis)")
    tables: List[str] = Field(default=["all"], description="Tabelas para importar: all, auxiliares, empresas, estabelecimentos, socios, simples")


class ETLValidationResponse(BaseModel):
    """ETL pre-validation response"""
    can_proceed: bool
    warnings: List[str] = []
    errors: List[str] = []
    disk_free_gb: float
    disk_used_gb: float
    postgres_running: bool
    tables_exist: bool


class ETLStatusResponse(BaseModel):
    """ETL status response"""
    job_id: str
    status: str  # idle, running, paused, completed, error
    current_step: Optional[str] = None
    current_file: Optional[str] = None
    current_table: Optional[str] = None
    progress_percent: float = 0.0
    files_processed: int = 0
    files_total: int = 0
    records_imported: int = 0
    disk_free_gb: Optional[float] = None
    disk_used_gb: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    elapsed_seconds: int = 0
    estimated_remaining_seconds: Optional[int] = None
    error_message: Optional[str] = None
    warnings: List[str] = []
    
    class Config:
        from_attributes = True


class ETLLogsResponse(BaseModel):
    """ETL logs response"""
    logs: List[str]
    total_lines: int


class ETLStartResponse(BaseModel):
    """Response when starting ETL"""
    status: str
    job_id: str
    message: str
