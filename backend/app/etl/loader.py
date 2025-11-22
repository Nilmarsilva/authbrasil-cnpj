"""
Loader Module
Loads processed data into PostgreSQL efficiently
"""

import logging
from typing import List, Dict, Any
from io import StringIO

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.empresa import Empresa, Estabelecimento, Socio

logger = logging.getLogger(__name__)


class DatabaseLoader:
    """Efficiently loads data into PostgreSQL"""
    
    # Mapping of file types to table names
    TABLE_MAPPINGS = {
        "Empresas": "empresas",
        "Estabelecimentos": "estabelecimentos",
        "Socios": "socios",
    }
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.inserted_counts = {}
    
    async def bulk_insert(
        self,
        file_type: str,
        records: List[Dict[str, Any]]
    ) -> int:
        """
        Bulk insert records using PostgreSQL COPY
        
        Args:
            file_type: Type of data (Empresas, Estabelecimentos, etc)
            records: List of records to insert
        
        Returns:
            Number of records inserted
        """
        table_name = self.TABLE_MAPPINGS.get(file_type)
        
        if not table_name:
            logger.warning(f"No table mapping for {file_type}")
            return 0
        
        if not records:
            return 0
        
        logger.info(f"Bulk inserting {len(records)} records into {table_name}")
        
        try:
            # Get column names from first record
            columns = list(records[0].keys())
            
            # Create CSV buffer
            buffer = StringIO()
            
            for record in records:
                # Convert record to CSV row
                values = []
                for col in columns:
                    value = record.get(col)
                    if value is None:
                        values.append('\\N')  # NULL in COPY format
                    else:
                        # Escape special characters
                        value_str = str(value).replace('\\', '\\\\').replace('\t', '\\t').replace('\n', '\\n')
                        values.append(value_str)
                
                buffer.write('\t'.join(values) + '\n')
            
            buffer.seek(0)
            
            # Use COPY for bulk insert (much faster than INSERT)
            copy_sql = f"""
                COPY {table_name} ({', '.join(columns)})
                FROM STDIN
                WITH (FORMAT text, DELIMITER E'\\t', NULL '\\N')
            """
            
            # Execute using raw connection
            conn = await self.session.connection()
            raw_conn = await conn.get_raw_connection()
            
            cursor = await raw_conn.driver_connection.cursor()
            await cursor.copy_expert(copy_sql, buffer)
            
            await self.session.commit()
            
            # Track inserted count
            if file_type not in self.inserted_counts:
                self.inserted_counts[file_type] = 0
            self.inserted_counts[file_type] += len(records)
            
            logger.info(f"✅ Inserted {len(records)} records into {table_name}")
            return len(records)
        
        except Exception as e:
            logger.error(f"Error bulk inserting into {table_name}: {e}")
            await self.session.rollback()
            raise
    
    async def truncate_table(self, file_type: str):
        """Truncate table before loading new data"""
        table_name = self.TABLE_MAPPINGS.get(file_type)
        
        if not table_name:
            return
        
        logger.warning(f"Truncating table {table_name}")
        
        try:
            await self.session.execute(text(f"TRUNCATE TABLE {table_name} CASCADE"))
            await self.session.commit()
            logger.info(f"✅ Truncated {table_name}")
        except Exception as e:
            logger.error(f"Error truncating {table_name}: {e}")
            await self.session.rollback()
            raise
    
    async def create_indexes(self):
        """Create/recreate indexes after bulk load"""
        logger.info("Creating indexes...")
        
        indexes = [
            # Empresas
            "CREATE INDEX IF NOT EXISTS idx_empresas_cnpj_basico ON empresas(cnpj_basico)",
            "CREATE INDEX IF NOT EXISTS idx_empresas_razao_social ON empresas USING gin(to_tsvector('portuguese', razao_social))",
            
            # Estabelecimentos
            "CREATE INDEX IF NOT EXISTS idx_estabelecimentos_cnpj_completo ON estabelecimentos(cnpj_completo)",
            "CREATE INDEX IF NOT EXISTS idx_estabelecimentos_cnpj_basico ON estabelecimentos(cnpj_basico)",
            "CREATE INDEX IF NOT EXISTS idx_estabelecimentos_uf_municipio ON estabelecimentos(uf, municipio)",
            "CREATE INDEX IF NOT EXISTS idx_estabelecimentos_situacao ON estabelecimentos(situacao_cadastral)",
            
            # Sócios
            "CREATE INDEX IF NOT EXISTS idx_socios_cnpj_basico ON socios(cnpj_basico)",
            "CREATE INDEX IF NOT EXISTS idx_socios_cpf_cnpj_socio ON socios(cpf_cnpj_socio)",
            "CREATE INDEX IF NOT EXISTS idx_socios_nome ON socios USING gin(to_tsvector('portuguese', nome_socio))",
        ]
        
        for index_sql in indexes:
            try:
                await self.session.execute(text(index_sql))
                logger.info(f"✅ Created: {index_sql.split('ON')[0].strip()}")
            except Exception as e:
                logger.warning(f"Index creation warning: {e}")
        
        await self.session.commit()
        logger.info("✅ Indexes created/updated")
    
    async def update_statistics(self):
        """Update table statistics for query optimization"""
        logger.info("Updating statistics...")
        
        tables = ["empresas", "estabelecimentos", "socios"]
        
        for table in tables:
            try:
                await self.session.execute(text(f"ANALYZE {table}"))
                logger.info(f"✅ Analyzed {table}")
            except Exception as e:
                logger.error(f"Error analyzing {table}: {e}")
        
        await self.session.commit()
        logger.info("✅ Statistics updated")
    
    def get_stats(self) -> Dict[str, int]:
        """Get insertion statistics"""
        return self.inserted_counts.copy()


# CLI usage
if __name__ == "__main__":
    import asyncio
    from app.db.session import async_session
    
    async def test_loader():
        async with async_session() as session:
            loader = DatabaseLoader(session)
            
            # Test with sample data
            sample_data = [
                {
                    "cnpj_basico": "12345678",
                    "razao_social": "EMPRESA TESTE LTDA",
                    "natureza_juridica": "2062",
                    "qualificacao_responsavel": "49",
                    "capital_social": "100000.00",
                    "porte_empresa": "3",
                    "ente_federativo_responsavel": None,
                }
            ]
            
            count = await loader.bulk_insert("Empresas", sample_data)
            print(f"✅ Inserted {count} test records")
            
            print("\nStats:", loader.get_stats())
    
    asyncio.run(test_loader())
