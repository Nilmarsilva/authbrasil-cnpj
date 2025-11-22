#!/usr/bin/env python
"""
Database Optimization Script
Configura VACUUM, ANALYZE, e otimizações do PostgreSQL
"""

import asyncio
import logging
from sqlalchemy import text
from app.db.session import async_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def configure_autovacuum():
    """Configura autovacuum para tabelas grandes"""
    logger.info("🔧 Configurando autovacuum...")
    
    async with async_session() as session:
        # Configurar autovacuum para tabelas grandes
        tables = [
            'empresas',
            'estabelecimentos',
            'socios',
            'simples',
        ]
        
        for table in tables:
            # Ajustar thresholds de autovacuum
            await session.execute(text(f"""
                ALTER TABLE {table} SET (
                    autovacuum_vacuum_scale_factor = 0.05,
                    autovacuum_vacuum_threshold = 10000,
                    autovacuum_analyze_scale_factor = 0.02,
                    autovacuum_analyze_threshold = 5000
                )
            """))
            logger.info(f"  ✅ Configurado autovacuum para {table}")
        
        await session.commit()


async def create_full_text_search_indexes():
    """Cria índices de busca full-text"""
    logger.info("📚 Criando índices de busca full-text...")
    
    async with async_session() as session:
        # Habilitar extensão pg_trgm (trigram similarity)
        await session.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        
        # Índice trigram para razão social
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_empresas_razao_social_trgm 
            ON empresas USING gin(razao_social gin_trgm_ops)
        """))
        logger.info("  ✅ Índice trigram em empresas.razao_social")
        
        # Índice trigram para nome fantasia
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_estabelecimentos_nome_fantasia_trgm 
            ON estabelecimentos USING gin(nome_fantasia gin_trgm_ops)
        """))
        logger.info("  ✅ Índice trigram em estabelecimentos.nome_fantasia")
        
        # Índice trigram para nome do sócio
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_socios_nome_socio_trgm 
            ON socios USING gin(nome_socio gin_trgm_ops)
        """))
        logger.info("  ✅ Índice trigram em socios.nome_socio")
        
        await session.commit()


async def create_composite_indexes():
    """Cria índices compostos para queries comuns"""
    logger.info("🔗 Criando índices compostos...")
    
    async with async_session() as session:
        # Índice composto para busca por UF + Situação
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_estabelecimentos_uf_situacao 
            ON estabelecimentos(uf, situacao_cadastral)
        """))
        logger.info("  ✅ Índice (uf, situacao_cadastral)")
        
        # Índice composto para busca por Município + CNAE
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_estabelecimentos_municipio_cnae 
            ON estabelecimentos(municipio, cnae_fiscal_principal)
        """))
        logger.info("  ✅ Índice (municipio, cnae_fiscal_principal)")
        
        # Índice composto para busca em empresas
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_empresas_natureza_porte 
            ON empresas(natureza_juridica, porte_empresa)
        """))
        logger.info("  ✅ Índice (natureza_juridica, porte_empresa)")
        
        await session.commit()


async def create_partial_indexes():
    """Cria índices parciais para queries específicas"""
    logger.info("🎯 Criando índices parciais...")
    
    async with async_session() as session:
        # Índice apenas para empresas ativas
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_estabelecimentos_ativos 
            ON estabelecimentos(cnpj_completo) 
            WHERE situacao_cadastral = '02'
        """))
        logger.info("  ✅ Índice parcial para estabelecimentos ativos")
        
        # Índice apenas para matrizes
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_estabelecimentos_matrizes 
            ON estabelecimentos(cnpj_basico) 
            WHERE identificador_matriz_filial = '1'
        """))
        logger.info("  ✅ Índice parcial para matrizes")
        
        # Índice apenas para optantes do Simples
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_simples_optantes 
            ON simples(cnpj_basico) 
            WHERE opcao_simples = 'S'
        """))
        logger.info("  ✅ Índice parcial para optantes Simples")
        
        # Índice apenas para MEI
        await session.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_simples_mei 
            ON simples(cnpj_basico) 
            WHERE opcao_mei = 'S'
        """))
        logger.info("  ✅ Índice parcial para MEI")
        
        await session.commit()


async def vacuum_analyze_all():
    """Executa VACUUM ANALYZE em todas as tabelas"""
    logger.info("🧹 Executando VACUUM ANALYZE...")
    
    async with async_session() as session:
        tables = [
            'cnaes', 'municipios', 'naturezas', 'paises', 
            'qualificacoes', 'motivos', 'simples',
            'empresas', 'estabelecimentos', 'socios'
        ]
        
        for table in tables:
            logger.info(f"  🔄 VACUUM ANALYZE {table}...")
            await session.execute(text(f"VACUUM ANALYZE {table}"))
            logger.info(f"  ✅ {table}")
        
        await session.commit()


async def show_table_stats():
    """Mostra estatísticas das tabelas"""
    logger.info("\n📊 Estatísticas das Tabelas:")
    logger.info("=" * 80)
    
    async with async_session() as session:
        result = await session.execute(text("""
            SELECT 
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
                n_live_tup as rows,
                n_dead_tup as dead_rows,
                last_vacuum,
                last_autovacuum,
                last_analyze,
                last_autoanalyze
            FROM pg_stat_user_tables
            WHERE schemaname = 'public'
            ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
        """))
        
        rows = result.fetchall()
        
        for row in rows:
            logger.info(f"\n📋 {row[1]}")
            logger.info(f"  Tamanho: {row[2]}")
            logger.info(f"  Linhas: {row[3]:,}")
            logger.info(f"  Linhas mortas: {row[4]:,}")
            logger.info(f"  Último VACUUM: {row[5] or 'Nunca'}")
            logger.info(f"  Último ANALYZE: {row[7] or 'Nunca'}")


async def main():
    """Executa todas as otimizações"""
    logger.info("🚀 Iniciando otimização do banco de dados")
    logger.info("=" * 80)
    
    try:
        # 1. Configurar autovacuum
        await configure_autovacuum()
        
        # 2. Criar índices full-text
        await create_full_text_search_indexes()
        
        # 3. Criar índices compostos
        await create_composite_indexes()
        
        # 4. Criar índices parciais
        await create_partial_indexes()
        
        # 5. VACUUM ANALYZE
        await vacuum_analyze_all()
        
        # 6. Mostrar estatísticas
        await show_table_stats()
        
        logger.info("\n" + "=" * 80)
        logger.info("✅ Otimização concluída com sucesso!")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"\n❌ Erro durante otimização: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
