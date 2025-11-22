"""
CNPJ Endpoints
Company data query endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.empresa import Estabelecimento, Empresa, Socio

router = APIRouter()


@router.get("/{cnpj}")
async def get_cnpj(cnpj: str, db: Session = Depends(get_db)):
    """
    Get complete CNPJ information
    
    Args:
        cnpj: CNPJ number (14 digits, with or without formatting)
        
    Returns:
        Complete company data including establishment and partners
    """
    # Clean CNPJ (remove formatting)
    cnpj_clean = ''.join(filter(str.isdigit, cnpj))
    
    # Validate CNPJ length
    if len(cnpj_clean) != 14:
        raise HTTPException(
            status_code=400,
            detail="CNPJ inválido. Deve conter 14 dígitos."
        )
    
    # Query establishment
    estabelecimento = db.query(Estabelecimento).filter(
        Estabelecimento.cnpj_completo == cnpj_clean
    ).first()
    
    if not estabelecimento:
        raise HTTPException(
            status_code=404,
            detail="CNPJ não encontrado na base de dados"
        )
    
    # Query empresa (matriz)
    empresa = db.query(Empresa).filter(
        Empresa.cnpj_basico == estabelecimento.cnpj_basico
    ).first()
    
    # Query socios
    socios = db.query(Socio).filter(
        Socio.cnpj_basico == estabelecimento.cnpj_basico
    ).all()
    
    return {
        "success": True,
        "data": {
            "cnpj": cnpj_clean,
            "razao_social": empresa.razao_social if empresa else None,
            "nome_fantasia": estabelecimento.nome_fantasia,
            "situacao_cadastral": estabelecimento.situacao_cadastral,
            "data_situacao_cadastral": estabelecimento.data_situacao_cadastral,
            "endereco": {
                "logradouro": estabelecimento.logradouro,
                "numero": estabelecimento.numero,
                "complemento": estabelecimento.complemento,
                "bairro": estabelecimento.bairro,
                "cep": estabelecimento.cep,
                "municipio": estabelecimento.municipio,
                "uf": estabelecimento.uf,
            },
            "contato": {
                "email": estabelecimento.email,
                "telefone_1": f"({estabelecimento.ddd_1}) {estabelecimento.telefone_1}" if estabelecimento.ddd_1 else None,
                "telefone_2": f"({estabelecimento.ddd_2}) {estabelecimento.telefone_2}" if estabelecimento.ddd_2 else None,
            },
            "atividade": {
                "cnae_principal": estabelecimento.cnae_fiscal_principal,
                "cnae_secundaria": estabelecimento.cnae_fiscal_secundaria,
            },
            "socios": [
                {
                    "nome": socio.nome_socio,
                    "cpf_cnpj": socio.cpf_cnpj_socio,
                    "qualificacao": socio.qualificacao_socio,
                    "data_entrada": socio.data_entrada_sociedade,
                }
                for socio in socios
            ],
            "capital_social": empresa.capital_social if empresa else None,
            "porte": empresa.porte_empresa if empresa else None,
            "natureza_juridica": empresa.natureza_juridica if empresa else None,
        },
        "metadata": {
            "cached": False,
            "timestamp": estabelecimento.updated_at.isoformat() if estabelecimento.updated_at else None,
        }
    }


@router.get("/search/razao-social")
async def search_by_razao_social(q: str, db: Session = Depends(get_db), limit: int = 10):
    """
    Search companies by razao social
    
    Args:
        q: Search query
        limit: Maximum number of results (default: 10, max: 100)
        
    Returns:
        List of matching companies
    """
    if len(q) < 3:
        raise HTTPException(
            status_code=400,
            detail="A busca deve conter pelo menos 3 caracteres"
        )
    
    # Limit maximum results
    limit = min(limit, 100)
    
    # Query empresas
    empresas = db.query(Empresa).filter(
        Empresa.razao_social.ilike(f"%{q}%")
    ).limit(limit).all()
    
    return {
        "success": True,
        "data": [
            {
                "cnpj_basico": empresa.cnpj_basico,
                "razao_social": empresa.razao_social,
                "natureza_juridica": empresa.natureza_juridica,
                "porte": empresa.porte_empresa,
            }
            for empresa in empresas
        ],
        "metadata": {
            "query": q,
            "results_count": len(empresas),
            "limit": limit,
        }
    }
