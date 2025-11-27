"""
Endpoints para insights adicionais de CNPJ
- Filiais de uma empresa
- Outras empresas de um sócio
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.db.session import get_async_db
from app.models.empresa import Empresa, Estabelecimento, Socio

router = APIRouter()


@router.get("/filiais/{cnpj_basico}")
async def get_filiais(
    cnpj_basico: str,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Busca todas as filiais de uma empresa pelo cnpj_basico.
    
    Args:
        cnpj_basico: CNPJ básico (8 dígitos)
        skip: Paginação - quantos pular
        limit: Paginação - quantos retornar (max 100)
    
    Returns:
        {
            "cnpj_basico": "12345678",
            "total_filiais": 50,
            "matriz": {...},
            "filiais": [...]
        }
    """
    # Validar cnpj_basico
    if len(cnpj_basico) != 8 or not cnpj_basico.isdigit():
        raise HTTPException(status_code=400, detail="CNPJ básico deve ter 8 dígitos")
    
    # Buscar matriz (identificador_matriz_filial = '1')
    result = await db.execute(
        select(Estabelecimento)
        .where(
            and_(
                Estabelecimento.cnpj_basico == cnpj_basico,
                Estabelecimento.identificador_matriz_filial == '1'
            )
        )
    )
    matriz = result.scalar_one_or_none()
    
    if not matriz:
        raise HTTPException(status_code=404, detail="CNPJ não encontrado")
    
    # Contar total de filiais (identificador_matriz_filial = '2')
    result = await db.execute(
        select(func.count())
        .select_from(Estabelecimento)
        .where(
            and_(
                Estabelecimento.cnpj_basico == cnpj_basico,
                Estabelecimento.identificador_matriz_filial == '2'
            )
        )
    )
    total_filiais = result.scalar()
    
    # Buscar filiais com paginação
    result = await db.execute(
        select(Estabelecimento)
        .where(
            and_(
                Estabelecimento.cnpj_basico == cnpj_basico,
                Estabelecimento.identificador_matriz_filial == '2'
            )
        )
        .offset(skip)
        .limit(min(limit, 100))
        .order_by(Estabelecimento.cnpj_ordem)
    )
    filiais = result.scalars().all()
    
    return {
        "cnpj_basico": cnpj_basico,
        "total_filiais": total_filiais,
        "matriz": {
            "cnpj_completo": matriz.cnpj_completo,
            "nome_fantasia": matriz.nome_fantasia,
            "uf": matriz.uf,
            "municipio": matriz.municipio,
            "situacao_cadastral": matriz.situacao_cadastral,
        },
        "filiais": [
            {
                "cnpj_completo": f.cnpj_completo,
                "cnpj_ordem": f.cnpj_ordem,
                "nome_fantasia": f.nome_fantasia,
                "uf": f.uf,
                "municipio": f.municipio,
                "situacao_cadastral": f.situacao_cadastral,
                "logradouro": f.logradouro,
                "numero": f.numero,
                "bairro": f.bairro,
                "cep": f.cep,
            }
            for f in filiais
        ]
    }


@router.get("/socio/{cpf_cnpj}/empresas")
async def get_empresas_socio(
    cpf_cnpj: str,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Busca todas as empresas em que um CPF/CNPJ participa como sócio.
    
    Args:
        cpf_cnpj: CPF (11 dígitos) ou CNPJ (14 dígitos) do sócio
        skip: Paginação
        limit: Limite (max 100)
    
    Returns:
        {
            "cpf_cnpj": "12345678900",
            "total_empresas": 5,
            "empresas": [...]
        }
    """
    # Validar CPF/CNPJ
    cpf_cnpj_limpo = cpf_cnpj.replace(".", "").replace("-", "").replace("/", "")
    
    if len(cpf_cnpj_limpo) not in [11, 14]:
        raise HTTPException(
            status_code=400, 
            detail="CPF deve ter 11 dígitos ou CNPJ 14 dígitos"
        )
    
    # Contar total de empresas
    result = await db.execute(
        select(func.count())
        .select_from(Socio)
        .where(Socio.cpf_cnpj_socio == cpf_cnpj_limpo)
    )
    total = result.scalar()
    
    if total == 0:
        raise HTTPException(
            status_code=404, 
            detail="Nenhuma empresa encontrada para este CPF/CNPJ"
        )
    
    # Buscar participações com JOIN em empresas e estabelecimentos
    result = await db.execute(
        select(
            Socio,
            Empresa,
            Estabelecimento
        )
        .join(Empresa, Socio.cnpj_basico == Empresa.cnpj_basico)
        .join(
            Estabelecimento,
            and_(
                Estabelecimento.cnpj_basico == Empresa.cnpj_basico,
                Estabelecimento.identificador_matriz_filial == '1'
            )
        )
        .where(Socio.cpf_cnpj_socio == cpf_cnpj_limpo)
        .offset(skip)
        .limit(min(limit, 100))
    )
    participacoes = result.all()
    
    empresas_list = []
    for socio, empresa, estabelecimento in participacoes:
        empresas_list.append({
            "cnpj_basico": empresa.cnpj_basico,
            "cnpj_completo": estabelecimento.cnpj_completo,
            "razao_social": empresa.razao_social,
            "nome_fantasia": estabelecimento.nome_fantasia,
            "qualificacao_socio": socio.qualificacao_socio,
            "data_entrada": socio.data_entrada_sociedade,
            "situacao_cadastral": estabelecimento.situacao_cadastral,
            "uf": estabelecimento.uf,
            "municipio": estabelecimento.municipio,
        })
    
    return {
        "cpf_cnpj": cpf_cnpj_limpo,
        "total_empresas": total,
        "empresas": empresas_list
    }


@router.get("/socio/nome/{nome}")
async def get_empresas_socio_por_nome(
    nome: str,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Busca empresas por nome do sócio (busca parcial).
    Útil quando não se tem o CPF.
    
    Args:
        nome: Nome do sócio (busca parcial, case-insensitive)
        skip: Paginação
        limit: Limite (max 50)
    
    Returns:
        Lista de sócios e suas empresas
    """
    if len(nome) < 3:
        raise HTTPException(
            status_code=400,
            detail="Nome deve ter no mínimo 3 caracteres"
        )
    
    # Buscar sócios por nome (case-insensitive, LIKE)
    result = await db.execute(
        select(
            Socio,
            Empresa,
            Estabelecimento
        )
        .join(Empresa, Socio.cnpj_basico == Empresa.cnpj_basico)
        .join(
            Estabelecimento,
            and_(
                Estabelecimento.cnpj_basico == Empresa.cnpj_basico,
                Estabelecimento.identificador_matriz_filial == '1'
            )
        )
        .where(Socio.nome_socio.ilike(f"%{nome}%"))
        .offset(skip)
        .limit(min(limit, 50))
    )
    participacoes = result.all()
    
    if not participacoes:
        raise HTTPException(
            status_code=404,
            detail="Nenhum sócio encontrado com este nome"
        )
    
    resultados = []
    for socio, empresa, estabelecimento in participacoes:
        resultados.append({
            "socio": {
                "nome": socio.nome_socio,
                "cpf_cnpj": socio.cpf_cnpj_socio,
                "qualificacao": socio.qualificacao_socio,
            },
            "empresa": {
                "cnpj_basico": empresa.cnpj_basico,
                "cnpj_completo": estabelecimento.cnpj_completo,
                "razao_social": empresa.razao_social,
                "nome_fantasia": estabelecimento.nome_fantasia,
                "uf": estabelecimento.uf,
                "municipio": estabelecimento.municipio,
            }
        })
    
    return {
        "total": len(resultados),
        "resultados": resultados
    }
