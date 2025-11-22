import zipfile
from pathlib import Path

pasta = Path("dados_pra_validar")

for zip_path in sorted(pasta.glob("*.zip")):
    print(f"\n{'='*60}")
    print(f"📦 {zip_path.name}")
    print(f"{'='*60}")
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for file_info in zf.filelist:
            print(f"  - {file_info.filename} ({file_info.file_size:,} bytes)")
