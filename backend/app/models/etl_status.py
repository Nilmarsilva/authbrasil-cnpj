"""
ETL Status Model
Tracks ETL job status and progress
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Float
from sqlalchemy.sql import func

from app.db.base import Base


class ETLStatus(Base):
    """
    ETL Status table for tracking import jobs
    """
    
    __tablename__ = "etl_status"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True, nullable=False)
    
    # Status: idle, running, paused, completed, error
    status = Column(String, default="idle", nullable=False)
    
    # Current progress
    current_step = Column(String)  # auxiliares, empresas, estabelecimentos, socios, simples
    current_file = Column(String)  # Estabelecimentos3.zip
    current_table = Column(String)  # estabelecimentos
    
    # Progress metrics
    progress_percent = Column(Float, default=0.0)
    files_processed = Column(Integer, default=0)
    files_total = Column(Integer, default=0)
    records_imported = Column(Integer, default=0)
    
    # Disk space
    disk_free_gb = Column(Float)
    disk_used_gb = Column(Float)
    
    # Timing
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    elapsed_seconds = Column(Integer, default=0)
    estimated_remaining_seconds = Column(Integer)
    
    # Error handling
    error_message = Column(String)
    warnings = Column(JSON)  # List of warning messages
    
    # Detailed state (for resume)
    job_metadata = Column(JSON)  # {processed_files: [...], failed_files: [...]}
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<ETLStatus(job_id={self.job_id}, status={self.status}, progress={self.progress_percent}%)>"
