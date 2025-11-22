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
        file_patterns: Optional[List[str]] = None,
        truncate_tables: bool = False
    ) -> dict:
        """
        Run the complete ETL pipeline
        
        Args:
            year_month: Format YYYY-MM (defaults to current month)
            file_patterns: List of patterns to filter files
            truncate_tables: Whether to truncate tables before loading
        
        Returns:
            Statistics dictionary
        """
        self.stats["start_time"] = datetime.now()
        
        logger.info("=" * 80)
        logger.info("Starting ETL Pipeline")
        logger.info(f"Year-Month: {year_month or 'current'}")
        logger.info(f"Patterns: {file_patterns or 'all'}")
        logger.info(f"Truncate: {truncate_tables}")
        logger.info("=" * 80)
        
        try:
            # Step 1: Download files
            logger.info("\n📥 STEP 1: Downloading files...")
            downloaded_files = await self.downloader.download_all(
                year_month=year_month,
                file_patterns=file_patterns
            )
            
            self.stats["files_downloaded"] = len(downloaded_files)
            
            if not downloaded_files:
                logger.error("No files downloaded, aborting")
                return self.stats
            
            # Step 2: Process and load
            logger.info(f"\n⚙️  STEP 2: Processing {len(downloaded_files)} files...")
            
            async with async_session() as session:
                loader = DatabaseLoader(session)
                
                # Truncate tables if requested
                if truncate_tables:
                    logger.info("\n🗑️  Truncating tables...")
                    for file_type in ["Empresas", "Estabelecimentos", "Socios"]:
                        await loader.truncate_table(file_type)
                
                # Process each ZIP file
                for i, zip_file in enumerate(downloaded_files, 1):
                    logger.info(f"\n📦 [{i}/{len(downloaded_files)}] Processing {zip_file.name}")
                    
                    try:
                        # Process and load in chunks
                        for file_type, chunk in self.processor.process_zip_file(zip_file):
                            # Skip if not main tables
                            if file_type not in ["Empresas", "Estabelecimentos", "Socios"]:
                                logger.debug(f"Skipping {file_type}")
                                continue
                            
                            # Bulk insert
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
