#!/usr/bin/env python
"""
Extract Samples - Extrai amostras dos dados para análise
Lê os ZIPs da pasta dados_pra_validar e extrai 50 linhas de cada
"""

import zipfile
import csv
from pathlib import Path


def extract_samples(source_dir="dados_pra_validar", output_dir="amostras", num_lines=50):
    """
    Extrai amostras dos arquivos ZIP
    
    Args:
        source_dir: Pasta com os ZIPs
        output_dir: Pasta para salvar as amostras
        num_lines: Número de linhas a extrair
    """
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    if not source_path.exists():
        print(f"❌ Pasta {source_dir} não encontrada!")
        return
    
    # Encontrar todos os ZIPs
    zip_files = list(source_path.glob("*.zip"))
    
    if not zip_files:
        print(f"❌ Nenhum arquivo ZIP encontrado em {source_dir}")
        return
    
    print(f"📦 Encontrados {len(zip_files)} arquivos ZIP")
    print("=" * 80)
    
    for zip_file in sorted(zip_files):
        print(f"\n📂 Processando: {zip_file.name}")
        
        try:
            with zipfile.ZipFile(zip_file, 'r') as zf:
                # Listar TODOS os arquivos dentro do ZIP (não pastas)
                csv_files = [f for f in zf.namelist() if not f.endswith('/')]
                
                if not csv_files:
                    print(f"  ⚠️  Nenhum arquivo encontrado em {zip_file.name}")
                    continue
                
                for csv_filename in csv_files:
                    print(f"\n  📄 {csv_filename}")
                    
                    # Criar nome do arquivo de saída
                    output_filename = f"{zip_file.stem}_{Path(csv_filename).stem}_sample.csv"
                    output_file = output_path / output_filename
                    
                    # Extrair amostra
                    with zf.open(csv_filename) as csv_file:
                        # Ler com encoding latin-1 (padrão da Receita)
                        lines = csv_file.read().decode('latin-1').splitlines()
                        
                        # Pegar primeiras N linhas
                        sample_lines = lines[:num_lines]
                        
                        # Salvar amostra
                        with open(output_file, 'w', encoding='utf-8') as out:
                            out.write('\n'.join(sample_lines))
                        
                        print(f"    ✅ Amostra salva: {output_file.name}")
                        print(f"    📊 Total de linhas no arquivo: {len(lines):,}")
                        print(f"    📋 Linhas na amostra: {len(sample_lines)}")
                        
                        # Mostrar estrutura (primeira linha)
                        if sample_lines:
                            first_line = sample_lines[0]
                            columns = first_line.split(';')
                            print(f"    🔢 Número de colunas: {len(columns)}")
                            print(f"    📝 Primeira linha (primeiros 200 chars):")
                            print(f"       {first_line[:200]}...")
        
        except Exception as e:
            print(f"  ❌ Erro ao processar {zip_file.name}: {e}")
    
    print("\n" + "=" * 80)
    print(f"✅ Amostras salvas em: {output_path.absolute()}")
    print("\n📋 Próximos passos:")
    print("  1. Abra os arquivos em 'amostras/' para ver a estrutura")
    print("  2. Identifique os campos de cada tipo de arquivo")
    print("  3. Crie os modelos SQLAlchemy baseado nos campos reais")


if __name__ == "__main__":
    extract_samples()
