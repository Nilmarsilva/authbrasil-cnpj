"""
ETL Orchestrator
Coordinates the entire ETL pipeline
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, List

from app.etl.downloader import ReceitaDownloader
from app.etl.processor import CSVProcessor
from app.etl.loader import DatabaseLoader
from app.db.session import async_session

logger = logging.getLogger(__name__)


class ETLOrchestrator:
    """Orchestrates the complete ETL pipeline"""
    
    def __init__(
        self,
        download_dir: str = "./data/receita",
        chunk_size: int = 100000,
        clean_after: bool = True
    ):
        self.download_dir = Path(download_dir)
        self.chunk_size = chunk_size
        self.clean_after = clean_after
        
        self.downloader = ReceitaDownloader(download_dir)
        self.processor = CSVProcessor(chunk_size)
        
        self.stats = {
            "start_time": None,
            "end_time": None,
            "files_downloaded": 0,
            "files_processed": 0,
            "total_records": 0,
            "errors": [],
        }
    
    async def run(
        self,
        year_month: Optional[str] = None,
        truncate_tables: bool = False
    ) -> dict:
        """
        Run the complete ETL pipeline
        
        IMPORTANTE: Baixa TODOS os 37 arquivos primeiro, depois processa em ordem
        
        Args:
            year_month: Format YYYY-MM (defaults to 2025-11)
            truncate_tables: Whether to truncate tables before loading
        
        Returns:
            Statistics dictionary
        """
        self.stats["start_time"] = datetime.now()
        
        if year_month is None:
            year_month = "2025-11"  # Último mês disponível
        
        logger.info("=" * 80)
        logger.info("Starting ETL Pipeline - FULL DOWNLOAD")
        logger.info(f"Year-Month: {year_month}")
        logger.info(f"Truncate: {truncate_tables}")
        logger.info("⚠️  IMPORTANTE: Baixando TODOS os 37 arquivos (~15-20GB)")
        logger.info("=" * 80)
        
        try:
            # Step 1: Download ALL files (no filter)
            logger.info("\n📥 STEP 1: Downloading ALL files...")
            logger.info("This will take 30-60 minutes depending on connection")
            downloaded_files = await self.downloader.download_all(
                year_month=year_month,
                file_patterns=None  # Baixar TUDO
            )
            
            self.stats["files_downloaded"] = len(downloaded_files)
            
            logger.info(f"\n✅ Downloaded {len(downloaded_files)} files")
            logger.info(f"Total size: {sum(f.stat().st_size for f in downloaded_files) / 1024**3:.2f} GB")
            
            if not downloaded_files:
                logger.error("No files downloaded, aborting")
                return self.stats
            
            # Step 2: Process and load IN ORDER
            logger.info(f"\n⚙️  STEP 2: Processing files in correct order...")
            
            # Ordem de processamento (respeita relacionamentos)
            processing_order = [
                # 1. Tabelas auxiliares (lookup tables)
                ("CNAEs", "cnaes"),
                ("Municipios", "municipios"),
                ("Naturezas", "naturezas"),
                ("Paises", "paises"),
                ("Qualificacoes", "qualificacoes"),
                ("Motivos", "motivos"),
                
                # 2. Dados principais (na ordem de dependência)
                ("Empresas", "empresas"),
                ("Estabelecimentos", "estabelecimentos"),
                ("Socios", "socios"),
                ("Simples", "simples"),
            ]
            
            async with async_session() as session:
                loader = DatabaseLoader(session)
                
                # Truncate ALL tables if requested
                if truncate_tables:
                    logger.info("\n🗑️  Truncating ALL tables...")
                    for file_type, _ in processing_order:
                        try:
                            await loader.truncate_table(file_type)
                        except Exception as e:
                            logger.warning(f"Could not truncate {file_type}: {e}")
                
                # Process files in order
                for file_type, table_name in processing_order:
                    logger.info(f"\n📊 Processing {file_type} -> {table_name}")
                    
                    # Find all ZIP files matching this type
                    matching_files = [
                        f for f in downloaded_files 
                        if file_type.upper() in f.name.upper()
                    ]
                    
                    if not matching_files:
                        logger.warning(f"⚠️  No files found for {file_type}")
                        continue
                    
                    logger.info(f"Found {len(matching_files)} file(s) for {file_type}")
                    
                    # Process each matching file
                    for i, zip_file in enumerate(matching_files, 1):
                        logger.info(f"  [{i}/{len(matching_files)}] {zip_file.name}")
                        
                        try:
                            # Process and load in chunks
                            for detected_type, chunk in self.processor.process_zip_file(zip_file):
                                if detected_type == file_type:
                                    inserted = await loader.bulk_insert(file_type, chunk)
                                    self.stats["total_records"] += inserted
                            
                            self.stats["files_processed"] += 1
                        
                        except Exception as e:
                            error_msg = f"Error processing {zip_file.name}: {e}"
                            logger.error(error_msg)
                            self.stats["errors"].append(error_msg)
                            continue
                
                # Step 3: Post-processing
                logger.info("\n🔧 STEP 3: Post-processing...")
                
                logger.info("Creating indexes...")
                await loader.create_indexes()
                
                logger.info("Updating statistics...")
                await loader.update_statistics()
                
                # Get final stats
                insert_stats = loader.get_stats()
                logger.info(f"\n📊 Insertion Statistics:")
                for table, count in insert_stats.items():
                    logger.info(f"  {table}: {count:,} records")
            
            # Step 4: Cleanup
            if self.clean_after:
                logger.info("\n🧹 STEP 4: Cleaning up temporary files...")
                self._cleanup_downloads(downloaded_files)
            
            self.stats["end_time"] = datetime.now()
            duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()
            
            logger.info("\n" + "=" * 80)
            logger.info("✅ ETL Pipeline Completed Successfully")
            logger.info(f"Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
            logger.info(f"Files Downloaded: {self.stats['files_downloaded']}")
            logger.info(f"Files Processed: {self.stats['files_processed']}")
            logger.info(f"Total Records: {self.stats['total_records']:,}")
            logger.info(f"Errors: {len(self.stats['errors'])}")
            logger.info("=" * 80)
            
            return self.stats
        
        except Exception as e:
            logger.error(f"\n❌ ETL Pipeline Failed: {e}", exc_info=True)
            self.stats["errors"].append(str(e))
            raise
    
    def _cleanup_downloads(self, files: List[Path]):
        """Remove downloaded ZIP files"""
        for file in files:
            try:
                file.unlink()
                logger.info(f"  Removed {file.name}")
            except Exception as e:
                logger.warning(f"  Failed to remove {file.name}: {e}")


# CLI usage
if __name__ == "__main__":
    import asyncio
    import sys
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    async def main():
        # Get year-month from args
        year_month = sys.argv[1] if len(sys.argv) > 1 else None
        
        # Create orchestrator
        orchestrator = ETLOrchestrator(
            download_dir="./data/receita",
            chunk_size=100000,
            clean_after=False  # Keep files for now
        )
        
        # Run ETL
        stats = await orchestrator.run(
            year_month=year_month,
            file_patterns=["Empresas", "Estabelecimentos", "Socios"],
            truncate_tables=True  # Fresh import
        )
        
        print("\n📊 Final Statistics:")
        print(f"  Duration: {(stats['end_time'] - stats['start_time']).total_seconds():.1f}s")
        print(f"  Files: {stats['files_processed']}/{stats['files_downloaded']}")
        print(f"  Records: {stats['total_records']:,}")
        print(f"  Errors: {len(stats['errors'])}")
    
    asyncio.run(main())
