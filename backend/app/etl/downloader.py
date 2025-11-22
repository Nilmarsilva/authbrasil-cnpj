"""
Downloader Module
Downloads ZIP files from Receita Federal open data
"""

import asyncio
import logging
from pathlib import Path
from typing import List
from datetime import datetime

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Base URL da Receita Federal
BASE_URL = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj"


class ReceitaDownloader:
    """Downloads CNPJ data from Receita Federal"""
    
    def __init__(self, download_dir: str = "./data/receita"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)
        
    async def list_available_files(self, year_month: str = None) -> List[str]:
        """
        List available files for a given month
        
        Args:
            year_month: Format YYYY-MM (e.g. "2025-11")
                       If None, uses current month
        
        Returns:
            List of file URLs
        """
        if year_month is None:
            year_month = datetime.now().strftime("%Y-%m")
        
        url = f"{BASE_URL}/{year_month}/"
        
        logger.info(f"Listing files from {url}")
        
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
            except httpx.HTTPError as e:
                logger.error(f"Failed to list files: {e}")
                return []
        
        # Parse HTML to find ZIP files
        soup = BeautifulSoup(response.text, 'html.parser')
        files = []
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.endswith('.zip'):
                files.append(f"{url}{href}")
        
        logger.info(f"Found {len(files)} ZIP files")
        return files
    
    async def download_file(
        self, 
        url: str, 
        dest_path: Path = None,
        progress_callback=None
    ) -> Path:
        """
        Download a single file with progress tracking
        
        Args:
            url: File URL
            dest_path: Destination path
            progress_callback: Function to call with (downloaded, total)
        
        Returns:
            Path to downloaded file
        """
        if dest_path is None:
            filename = url.split('/')[-1]
            dest_path = self.download_dir / filename
        
        # Skip if file already exists
        if dest_path.exists():
            logger.info(f"File already exists: {dest_path}")
            return dest_path
        
        logger.info(f"Downloading {url} to {dest_path}")
        
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream('GET', url) as response:
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(dest_path, 'wb') as f:
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress_callback(downloaded, total_size)
        
        logger.info(f"Downloaded {dest_path} ({downloaded} bytes)")
        return dest_path
    
    async def download_all(
        self, 
        year_month: str = None,
        file_patterns: List[str] = None
    ) -> List[Path]:
        """
        Download all files for a given month
        
        Args:
            year_month: Format YYYY-MM
            file_patterns: List of patterns to filter files
                          e.g. ["Empresas", "Estabelecimentos", "Socios"]
        
        Returns:
            List of downloaded file paths
        """
        files = await self.list_available_files(year_month)
        
        # Filter by patterns if provided
        if file_patterns:
            files = [
                f for f in files 
                if any(pattern in f for pattern in file_patterns)
            ]
        
        logger.info(f"Downloading {len(files)} files...")
        
        downloaded_files = []
        
        for i, file_url in enumerate(files, 1):
            logger.info(f"[{i}/{len(files)}] {file_url}")
            
            def progress(downloaded, total):
                percent = (downloaded / total) * 100
                print(f"\r  Progress: {percent:.1f}%", end='', flush=True)
            
            try:
                path = await self.download_file(file_url, progress_callback=progress)
                downloaded_files.append(path)
                print()  # New line after progress
            except Exception as e:
                logger.error(f"Failed to download {file_url}: {e}")
        
        logger.info(f"Downloaded {len(downloaded_files)} files successfully")
        return downloaded_files


# CLI usage
if __name__ == "__main__":
    import sys
    
    async def main():
        downloader = ReceitaDownloader()
        
        # Get year-month from args or use current
        year_month = sys.argv[1] if len(sys.argv) > 1 else None
        
        # Download all files
        files = await downloader.download_all(
            year_month=year_month,
            file_patterns=["Empresas", "Estabelecimentos", "Socios"]
        )
        
        print(f"\n✅ Downloaded {len(files)} files to {downloader.download_dir}")
    
    asyncio.run(main())
