#!/usr/bin/env python
"""
ETL Command Line Interface
Run the ETL pipeline manually

Usage:
    python run_etl.py                  # Current month
    python run_etl.py 2025-11          # Specific month
    python run_etl.py --help           # Show help
"""

import asyncio
import argparse
import logging
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.etl.orchestrator import ETLOrchestrator


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('etl.log', encoding='utf-8')
        ]
    )


async def run_etl(args):
    """Run ETL with given arguments"""
    
    orchestrator = ETLOrchestrator(
        download_dir=args.download_dir,
        chunk_size=args.chunk_size,
        clean_after=args.clean
    )
    
    # Parse file patterns
    file_patterns = None
    if args.files:
        file_patterns = args.files.split(',')
    
    # Run ETL
    stats = await orchestrator.run(
        year_month=args.month,
        file_patterns=file_patterns,
        truncate_tables=args.truncate
    )
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 ETL Summary")
    print("=" * 80)
    print(f"Start Time:       {stats['start_time']}")
    print(f"End Time:         {stats['end_time']}")
    print(f"Duration:         {(stats['end_time'] - stats['start_time']).total_seconds():.1f}s")
    print(f"Files Downloaded: {stats['files_downloaded']}")
    print(f"Files Processed:  {stats['files_processed']}")
    print(f"Total Records:    {stats['total_records']:,}")
    print(f"Errors:           {len(stats['errors'])}")
    
    if stats['errors']:
        print("\n⚠️  Errors:")
        for error in stats['errors']:
            print(f"  - {error}")
    
    print("=" * 80)
    
    return 0 if not stats['errors'] else 1


def main():
    parser = argparse.ArgumentParser(
        description='ETL Pipeline for Receita Federal CNPJ data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download and process current month
  python run_etl.py
  
  # Process specific month
  python run_etl.py --month 2025-11
  
  # Process only specific files
  python run_etl.py --files "Empresas,Estabelecimentos"
  
  # Truncate tables before loading
  python run_etl.py --truncate
  
  # Keep downloaded files
  python run_etl.py --no-clean
        """
    )
    
    parser.add_argument(
        'month',
        nargs='?',
        help='Year-month to process (YYYY-MM). Defaults to current month'
    )
    
    parser.add_argument(
        '--files',
        help='Comma-separated list of file patterns to process (e.g. "Empresas,Socios")'
    )
    
    parser.add_argument(
        '--truncate',
        action='store_true',
        help='Truncate tables before loading'
    )
    
    parser.add_argument(
        '--no-clean',
        dest='clean',
        action='store_false',
        help='Keep downloaded files after processing'
    )
    
    parser.add_argument(
        '--download-dir',
        default='./data/receita',
        help='Directory to download files to (default: ./data/receita)'
    )
    
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=100000,
        help='Number of records to process per chunk (default: 100000)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Run ETL
    try:
        exit_code = asyncio.run(run_etl(args))
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  ETL interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n❌ ETL failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
