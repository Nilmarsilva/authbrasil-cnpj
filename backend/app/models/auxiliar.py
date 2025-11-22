"""
Auxiliary Tables Models
Lookup tables from Receita Federal
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.db.base import Base


class CNAE(Base):
    """CNAEs table - Economic activity codes"""
    
    __tablename__ = "cnaes"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(7), unique=True, index=True, nullable=False)
    descricao = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Municipio(Base):
    """Municipios table - Brazilian cities (IBGE codes)"""
    
    __tablename__ = "municipios"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(4), unique=True, index=True, nullable=False)
    descricao = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Natureza(Base):
    """Naturezas table - Legal nature codes"""
    
    __tablename__ = "naturezas"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(4), unique=True, index=True, nullable=False)
    descricao = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Pais(Base):
    """Paises table - Countries"""
    
    __tablename__ = "paises"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(3), unique=True, index=True, nullable=False)
    descricao = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Qualificacao(Base):
    """Qualificacoes table - Partner qualifications"""
    
    __tablename__ = "qualificacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(2), unique=True, index=True, nullable=False)
    descricao = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Motivo(Base):
    """Motivos table - Cadastral situation reasons"""
    
    __tablename__ = "motivos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(2), unique=True, index=True, nullable=False)
    descricao = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Simples(Base):
    """Simples table - Simples Nacional e MEI optants"""
    
    __tablename__ = "simples"
    
    __table_args__ = (
        Index('idx_simples_opcao_simples', 'opcao_simples'),
        Index('idx_simples_opcao_mei', 'opcao_mei'),
        {'comment': 'Optantes do Simples Nacional e MEI'}
    )
    
    id = Column(Integer, primary_key=True, index=True)
    cnpj_basico = Column(String(8), unique=True, index=True, nullable=False, comment="CNPJ básico (liga com empresas)")
    opcao_simples = Column(String(1), nullable=True, comment="S=Optante Simples, N=Não Optante")
    data_opcao_simples = Column(String(8), nullable=True, comment="Data opção Simples (YYYYMMDD)")
    data_exclusao_simples = Column(String(8), nullable=True, comment="Data exclusão Simples (YYYYMMDD)")
    opcao_mei = Column(String(1), nullable=True, comment="S=Optante MEI, N=Não Optante")
    data_opcao_mei = Column(String(8), nullable=True, comment="Data opção MEI (YYYYMMDD)")
    data_exclusao_mei = Column(String(8), nullable=True, comment="Data exclusão MEI (YYYYMMDD)")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
