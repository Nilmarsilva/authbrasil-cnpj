"""
Processor Module
Processes CSV files from Receita Federal in chunks
"""

import csv
import logging
import zipfile
from pathlib import Path
from typing import Iterator, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ProcessingStats:
    """Statistics for ETL processing"""
    total_records: int = 0
    processed_records: int = 0
    skipped_records: int = 0
    errors: int = 0


class CSVProcessor:
    """Process CSV files from Receita Federal"""
    
    # Column mappings for each file type
    COLUMN_MAPPINGS = {
        "CNAEs": {
            0: "codigo",
            1: "descricao",
        },
        "Municipios": {
            0: "codigo",
            1: "descricao",
        },
        "Naturezas": {
            0: "codigo",
            1: "descricao",
        },
        "Paises": {
            0: "codigo",
            1: "descricao",
        },
        "Qualificacoes": {
            0: "codigo",
            1: "descricao",
        },
        "Motivos": {
            0: "codigo",
            1: "descricao",
        },
        "Simples": {
            0: "cnpj_basico",
            1: "opcao_simples",
            2: "data_opcao_simples",
            3: "data_exclusao_simples",
            4: "opcao_mei",
            5: "data_opcao_mei",
            6: "data_exclusao_mei",
        },
        "Empresas": {
            0: "cnpj_basico",
            1: "razao_social",
            2: "natureza_juridica",
            3: "qualificacao_responsavel",
            4: "capital_social",
            5: "porte_empresa",
            6: "ente_federativo_responsavel",
        },
        "Estabelecimentos": {
            0: "cnpj_basico",
            1: "cnpj_ordem",
            2: "cnpj_dv",
            3: "identificador_matriz_filial",
            4: "nome_fantasia",
            5: "situacao_cadastral",
            6: "data_situacao_cadastral",
            7: "motivo_situacao_cadastral",
            8: "cidade_exterior",
            9: "pais",
            10: "data_inicio_atividade",
            11: "cnae_fiscal_principal",
            12: "cnae_fiscal_secundaria",
            13: "tipo_logradouro",
            14: "logradouro",
            15: "numero",
            16: "complemento",
            17: "bairro",
            18: "cep",
            19: "uf",
            20: "municipio",
            21: "ddd_1",
            22: "telefone_1",
            23: "ddd_2",
            24: "telefone_2",
            25: "ddd_fax",
            26: "fax",
            27: "email",
            28: "situacao_especial",
            29: "data_situacao_especial",
        },
        "Socios": {
            0: "cnpj_basico",
            1: "identificador_socio",
            2: "nome_socio",
            3: "cpf_cnpj_socio",
            4: "qualificacao_socio",
            5: "data_entrada_sociedade",
            6: "pais",
            7: "representante_legal",
            8: "nome_representante",
            9: "qualificacao_representante",
            10: "faixa_etaria",
        },
    }
    
    def __init__(self, chunk_size: int = 100000):
        self.chunk_size = chunk_size
        self.stats = ProcessingStats()
    
    def extract_zip(self, zip_path: Path, extract_to: Path = None) -> Path:
        """Extract ZIP file to temporary directory"""
        if extract_to is None:
            extract_to = zip_path.parent / zip_path.stem
        
        logger.info(f"Extracting {zip_path} to {extract_to}")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        
        return extract_to
    
    def detect_file_type(self, filename: str) -> str:
        """Detect file type from filename"""
        filename_upper = filename.upper()
        
        if "EMPRESA" in filename_upper:
            return "Empresas"
        elif "ESTABELE" in filename_upper:
            return "Estabelecimentos"
        elif "SOCIO" in filename_upper:
            return "Socios"
        elif "SIMPLES" in filename_upper:
            return "Simples"
        elif "CNAE" in filename_upper:
            return "CNAEs"
        elif "MOTI" in filename_upper:
            return "Motivos"
        elif "MUNIC" in filename_upper:
            return "Municipios"
        elif "NATUR" in filename_upper:
            return "Naturezas"
        elif "PAIS" in filename_upper:
            return "Paises"
        elif "QUALI" in filename_upper:
            return "Qualificacoes"
        
        return "Unknown"
    
    def process_csv_chunk(
        self,
        csv_path: Path,
        file_type: str = None
    ) -> Iterator[list[Dict[str, Any]]]:
        """
        Process CSV file in chunks
        
        Args:
            csv_path: Path to CSV file
            file_type: Type of file (Empresas, Estabelecimentos, etc)
        
        Yields:
            Chunks of records as list of dicts
        """
        if file_type is None:
            file_type = self.detect_file_type(csv_path.name)
        
        logger.info(f"Processing {csv_path} as {file_type}")
        
        column_mapping = self.COLUMN_MAPPINGS.get(file_type, {})
        
        if not column_mapping:
            logger.warning(f"No column mapping for {file_type}, skipping...")
            return
        
        chunk = []
        
        with open(csv_path, 'r', encoding='latin-1') as f:
            reader = csv.reader(f, delimiter=';', quotechar='"')
            
            for row_num, row in enumerate(reader, 1):
                try:
                    # Map columns to dict
                    record = {}
                    for idx, column_name in column_mapping.items():
                        if idx < len(row):
                            value = row[idx].strip()
                            # Convert empty strings to None
                            record[column_name] = value if value else None
                    
                    # Add computed fields
                    if file_type == "Estabelecimentos":
                        # Generate full CNPJ
                        if all(k in record for k in ['cnpj_basico', 'cnpj_ordem', 'cnpj_dv']):
                            record['cnpj_completo'] = (
                                f"{record['cnpj_basico']}"
                                f"{record['cnpj_ordem']}"
                                f"{record['cnpj_dv']}"
                            )
                    
                    chunk.append(record)
                    self.stats.processed_records += 1
                    
                    # Yield chunk when full
                    if len(chunk) >= self.chunk_size:
                        logger.info(f"Yielding chunk of {len(chunk)} records (total: {self.stats.processed_records})")
                        yield chunk
                        chunk = []
                
                except Exception as e:
                    logger.error(f"Error processing row {row_num}: {e}")
                    self.stats.errors += 1
                    continue
        
        # Yield remaining records
        if chunk:
            logger.info(f"Yielding final chunk of {len(chunk)} records")
            yield chunk
    
    def process_zip_file(self, zip_path: Path) -> Iterator[tuple[str, list[Dict[str, Any]]]]:
        """
        Process all CSVs in a ZIP file
        
        Yields:
            Tuples of (file_type, records_chunk)
        """
        # Extract ZIP
        extract_dir = self.extract_zip(zip_path)
        
        try:
            # Find all CSV files
            csv_files = list(extract_dir.glob("*.csv")) + list(extract_dir.glob("**/*.csv"))
            
            logger.info(f"Found {len(csv_files)} CSV files in {zip_path.name}")
            
            for csv_file in csv_files:
                file_type = self.detect_file_type(csv_file.name)
                
                for chunk in self.process_csv_chunk(csv_file, file_type):
                    yield (file_type, chunk)
        
        finally:
            # Cleanup extracted files
            import shutil
            if extract_dir.exists():
                shutil.rmtree(extract_dir)
                logger.info(f"Cleaned up {extract_dir}")


# CLI usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python processor.py <zip_file>")
        sys.exit(1)
    
    zip_path = Path(sys.argv[1])
    
    processor = CSVProcessor(chunk_size=10000)  # Smaller chunks for testing
    
    for file_type, chunk in processor.process_zip_file(zip_path):
        print(f"\n{file_type}: {len(chunk)} records")
        # Show first record as sample
        if chunk:
            print("Sample:", chunk[0])
    
    print(f"\n✅ Stats:")
    print(f"  Processed: {processor.stats.processed_records:,}")
    print(f"  Errors: {processor.stats.errors:,}")
