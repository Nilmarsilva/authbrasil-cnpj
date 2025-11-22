"""
Empresa Models
CNPJ data models from Receita Federal
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, Index, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Empresa(Base):
    """Empresas table - CNPJ root data (matriz)"""
    
    __tablename__ = "empresas"
    
    id = Column(Integer, primary_key=True, index=True)
    cnpj_basico = Column(String(8), unique=True, index=True, nullable=False)
    razao_social = Column(String, nullable=True)
    natureza_juridica = Column(String(4), nullable=True)
    qualificacao_responsavel = Column(String(2), nullable=True)
    capital_social = Column(String, nullable=True)
    porte_empresa = Column(String(2), nullable=True)
    ente_federativo_responsavel = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    estabelecimentos = relationship("Estabelecimento", back_populates="empresa")
    socios = relationship("Socio", back_populates="empresa")


class Estabelecimento(Base):
    """Estabelecimentos table - CNPJ establishment data (filiais)"""
    
    __tablename__ = "estabelecimentos"
    
    id = Column(Integer, primary_key=True, index=True)
    cnpj_basico = Column(String(8), ForeignKey("empresas.cnpj_basico"), index=True, nullable=False)
    cnpj_ordem = Column(String(4), nullable=False)
    cnpj_dv = Column(String(2), nullable=False)
    cnpj_completo = Column(String(14), unique=True, index=True, nullable=False)
    
    # Establishment details
    identificador_matriz_filial = Column(String(1), nullable=True)
    nome_fantasia = Column(String, nullable=True)
    situacao_cadastral = Column(String(2), nullable=True)
    data_situacao_cadastral = Column(Date, nullable=True)
    motivo_situacao_cadastral = Column(String(2), nullable=True)
    
    # Address
    tipo_logradouro = Column(String, nullable=True)
    logradouro = Column(String, nullable=True)
    numero = Column(String, nullable=True)
    complemento = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    cep = Column(String(8), nullable=True)
    uf = Column(String(2), nullable=True)
    municipio = Column(String(4), nullable=True)
    
    # Contact
    ddd_1 = Column(String(4), nullable=True)
    telefone_1 = Column(String(8), nullable=True)
    ddd_2 = Column(String(4), nullable=True)
    telefone_2 = Column(String(8), nullable=True)
    email = Column(String, nullable=True)
    
    # Activity
    cnae_fiscal_principal = Column(String(7), nullable=True)
    cnae_fiscal_secundaria = Column(String, nullable=True)
    
    # Dates
    data_inicio_atividade = Column(Date, nullable=True)
    situacao_especial = Column(String, nullable=True)
    data_situacao_especial = Column(Date, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    empresa = relationship("Empresa", back_populates="estabelecimentos")
    
    # Indexes for common queries
    __table_args__ = (
        Index('idx_cnpj_completo', 'cnpj_completo'),
        Index('idx_razao_social_search', 'cnpj_basico'),
        Index('idx_uf_municipio', 'uf', 'municipio'),
    )


class Socio(Base):
    """Socios table - Company partners/shareholders"""
    
    __tablename__ = "socios"
    
    id = Column(Integer, primary_key=True, index=True)
    cnpj_basico = Column(String(8), ForeignKey("empresas.cnpj_basico"), index=True, nullable=False)
    identificador_socio = Column(String(1), nullable=True)
    nome_socio = Column(String, nullable=True)
    cpf_cnpj_socio = Column(String(14), nullable=True)
    qualificacao_socio = Column(String(2), nullable=True)
    data_entrada_sociedade = Column(Date, nullable=True)
    pais = Column(String(3), nullable=True)
    representante_legal = Column(String, nullable=True)
    nome_representante = Column(String, nullable=True)
    qualificacao_representante = Column(String(2), nullable=True)
    faixa_etaria = Column(String(1), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    empresa = relationship("Empresa", back_populates="socios")
    
    # Index for searches
    __table_args__ = (
        Index('idx_socio_nome', 'nome_socio'),
        Index('idx_socio_cpf_cnpj', 'cpf_cnpj_socio'),
    )
