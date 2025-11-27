"""
ETL Worker V2
Optimized ETL worker with lessons learned
- PostgreSQL COPY with LATIN1 encoding
- Automatic ZIP cleanup after processing
- Real-time progress tracking
- Resumable state
"""

import subprocess
import os
import shutil
import time
import logging
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models.etl_status import ETLStatus
from app.db.session import async_session

# Configuração
BASE_URL = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/"
DATA_DIR = Path("/root/data/receita")

# Container name - usar variável de ambiente ou buscar dinamicamente
import subprocess as sp
try:
    result = sp.run(
        ["docker", "ps", "--filter", "name=postgres", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
        timeout=5
    )
    CONTAINER_NAME = result.stdout.strip().split('\n')[0] if result.stdout else "databases_postgres.1.mrttx12uwquw44ho80kojdweo"
except Exception:
    CONTAINER_NAME = "databases_postgres.1.mrttx12uwquw44ho80kojdweo"

DB_USER = "authbrasil_user"
DB_NAME = "authbrasil_cnpj"

# Arquivos a processar (em ordem)
FILES_CONFIG = {
    "auxiliares": [
        ("Cnaes.zip", "F.K03200$W.CNAECSV", "cnaes", "codigo,descricao"),
        ("Motivos.zip", "F.K03200$W.MOTICSV.D51108", "motivos", "codigo,descricao"),
        ("Municipios.zip", "F.K03200$W.MUNICCSV.D51108", "municipios", "codigo,descricao"),
        ("Naturezas.zip", "F.K03200$W.NATJUCSV.D51108", "naturezas", "codigo,descricao"),
        ("Paises.zip", "F.K03200$W.PAISCSV", "paises", "codigo,descricao"),
        ("Qualificacoes.zip", "F.K03200$W.QUALSCSV.D51108", "qualificacoes", "codigo,descricao"),
    ],
    "empresas": [
        (f"Empresas{i}.zip", f"K3241.K03200Y{i}.D51108.EMPRECSV", "empresas", 
         "cnpj_basico,razao_social,natureza_juridica,qualificacao_responsavel,capital_social,porte_empresa,ente_federativo_responsavel")
        for i in range(10)
    ],
    "estabelecimentos": [
        (f"Estabelecimentos{i}.zip", f"K3241.K03200Y{i}.D51108.ESTABELE", "estabelecimentos",
         "cnpj_basico,cnpj_ordem,cnpj_dv,identificador_matriz_filial,nome_fantasia,situacao_cadastral,data_situacao_cadastral,motivo_situacao_cadastral,cidade_exterior,pais,data_inicio_atividade,cnae_fiscal_principal,cnae_fiscal_secundaria,tipo_logradouro,logradouro,numero,complemento,bairro,cep,uf,municipio,ddd_1,telefone_1,ddd_2,telefone_2,ddd_fax,fax,email,situacao_especial,data_situacao_especial")
        for i in range(10)
    ],
    "socios": [
        (f"Socios{i}.zip", f"K3241.K03200Y{i}.D51108.SOCIOCSV", "socios",
         "cnpj_basico,identificador_socio,nome_socio,cpf_cnpj_socio,qualificacao_socio,data_entrada_sociedade,pais,cpf_representante_legal,nome_representante_legal,qualificacao_representante_legal,faixa_etaria")
        for i in range(10)
    ],
    "simples": [
        ("Simples.zip", "K3241.K03200DV.D51108.SIMPLES.CSV.D51108", "simples",
         "cnpj_basico,opcao_simples,data_opcao_simples,data_exclusao_simples,opcao_mei,data_opcao_mei,data_exclusao_mei")
    ],
}

logger = logging.getLogger(__name__)


class ETLWorker:
    """ETL Worker with optimized COPY strategy"""
    
    def __init__(self, job_id: str, skip_download: bool = False, tables: List[str] = None):
        self.job_id = job_id
        self.skip_download = skip_download
        self.tables = tables or ["all"]
        self.start_time = time.time()
        self.files_processed = 0
        self.files_total = 0
        self.records_imported = 0
        
    async def update_status(self, **kwargs):
        """Update ETL status in database"""
        async with async_session() as db:
            await db.execute(
                update(ETLStatus)
                .where(ETLStatus.job_id == self.job_id)
                .values(**kwargs, updated_at=datetime.utcnow())
            )
            await db.commit()
    
    def get_disk_space(self):
        """Get disk space in GB"""
        stat = os.statvfs('/')
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        used_gb = ((stat.f_blocks - stat.f_bfree) * stat.f_frsize) / (1024**3)
        return free_gb, used_gb
    
    async def run(self):
        """Run complete ETL process"""
        try:
            await self.update_status(
                status="running",
                started_at=datetime.utcnow()
            )
            
            # Calculate total files
            self.files_total = sum(
                len(files) for table_name, files in FILES_CONFIG.items()
                if "all" in self.tables or table_name in self.tables
            )
            
            await self.update_status(files_total=self.files_total)
            
            # Process each table group
            for table_group, files in FILES_CONFIG.items():
                if "all" not in self.tables and table_group not in self.tables:
                    continue
                
                logger.info(f"Processing {table_group}...")
                await self.update_status(current_step=table_group)
                
                for zip_file, csv_pattern, table_name, columns in files:
                    await self.process_file(zip_file, csv_pattern, table_name, columns)
            
            # Post-processing
            await self.post_process()
            
            # Mark as completed
            await self.update_status(
                status="completed",
                completed_at=datetime.utcnow(),
                progress_percent=100.0,
                elapsed_seconds=int(time.time() - self.start_time)
            )
            
            logger.info(f"ETL completed! Total records: {self.records_imported}")
            
        except Exception as e:
            logger.error(f"ETL error: {e}", exc_info=True)
            await self.update_status(
                status="error",
                error_message=str(e),
                completed_at=datetime.utcnow()
            )
            raise
    
    async def process_file(self, zip_file: str, csv_pattern: str, table_name: str, columns: str):
        """Process a single ZIP file"""
        zip_path = DATA_DIR / zip_file
        extract_dir = DATA_DIR / zip_file.replace('.zip', '')
        
        try:
            # Update status
            await self.update_status(
                current_file=zip_file,
                current_table=table_name
            )
            
            free_gb, used_gb = self.get_disk_space()
            await self.update_status(disk_free_gb=free_gb, disk_used_gb=used_gb)
            
            # Extract ZIP
            logger.info(f"Extracting {zip_file}...")
            subprocess.run(
                ["unzip", "-o", str(zip_path), "-d", str(extract_dir)],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Find CSV file
            csv_files = list(extract_dir.glob(f"{csv_pattern}*"))
            if not csv_files:
                raise FileNotFoundError(f"CSV not found in {zip_file} with pattern {csv_pattern}")
            
            csv_file = csv_files[0]
            logger.info(f"Importing {csv_file.name} to {table_name}...")
            
            # Copy to container
            tmp_file = f"/tmp/{csv_file.name}"
            subprocess.run(
                ["docker", "cp", str(csv_file), f"{CONTAINER_NAME}:{tmp_file}"],
                check=True,
                stdout=subprocess.DEVNULL
            )
            
            # Execute COPY
            copy_cmd = f"""COPY {table_name}({columns}) FROM '{tmp_file}' WITH (FORMAT csv, DELIMITER ';', QUOTE '"', ENCODING 'LATIN1', HEADER false)"""
            
            result = subprocess.run(
                [
                    "docker", "exec", CONTAINER_NAME,
                    "psql", "-U", DB_USER, "-d", DB_NAME,
                    "-c", copy_cmd
                ],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse result
            if "COPY" in result.stdout:
                count_str = result.stdout.strip().split("COPY ")[-1]
                try:
                    count = int(count_str)
                    self.records_imported += count
                    logger.info(f"✅ {zip_file} - COPY {count}")
                except ValueError:
                    pass
            
            # Cleanup container
            subprocess.run(
                ["docker", "exec", CONTAINER_NAME, "rm", tmp_file],
                stderr=subprocess.DEVNULL
            )
            
            # Cleanup host
            shutil.rmtree(extract_dir, ignore_errors=True)
            zip_path.unlink(missing_ok=True)
            logger.info(f"🗑️  Deleted {zip_file}")
            
            # Update progress
            self.files_processed += 1
            progress = (self.files_processed / self.files_total) * 100
            elapsed = int(time.time() - self.start_time)
            
            if self.files_processed > 0:
                avg_time_per_file = elapsed / self.files_processed
                remaining_files = self.files_total - self.files_processed
                estimated_remaining = int(avg_time_per_file * remaining_files)
            else:
                estimated_remaining = None
            
            await self.update_status(
                files_processed=self.files_processed,
                progress_percent=round(progress, 2),
                records_imported=self.records_imported,
                elapsed_seconds=elapsed,
                estimated_remaining_seconds=estimated_remaining
            )
            
        except Exception as e:
            logger.error(f"Error processing {zip_file}: {e}")
            # Cleanup on error
            shutil.rmtree(extract_dir, ignore_errors=True)
            raise
    
    async def post_process(self):
        """Post-processing: update cnpj_completo, VACUUM, etc."""
        logger.info("Running post-processing...")
        
        await self.update_status(
            current_step="post_processing",
            current_file="Atualizando cnpj_completo..."
        )
        
        # Update cnpj_completo
        subprocess.run([
            "docker", "exec", CONTAINER_NAME,
            "psql", "-U", DB_USER, "-d", DB_NAME,
            "-c", "UPDATE estabelecimentos SET cnpj_completo = cnpj_basico || cnpj_ordem || cnpj_dv WHERE cnpj_completo IS NULL;"
        ], check=True)
        
        logger.info("✅ cnpj_completo updated")
        
        # VACUUM ANALYZE
        await self.update_status(current_file="VACUUM ANALYZE...")
        subprocess.run([
            "docker", "exec", CONTAINER_NAME,
            "psql", "-U", DB_USER, "-d", DB_NAME,
            "-c", "VACUUM ANALYZE;"
        ], check=True)
        
        logger.info("✅ VACUUM ANALYZE completed")
