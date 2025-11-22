"""
Empresa Models
CNPJ data models from Receita Federal
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Index, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Empresa(Base):
    """Empresa model - Dados da matriz (CNPJ básico)"""
    
    __tablename__ = "empresas"
    
    id = Column(Integer, primary_key=True, index=True)
    cnpj_basico = Column(String(8), unique=True, index=True, nullable=False, comment="CNPJ básico (8 dígitos)")
    razao_social = Column(String, nullable=False, index=True, comment="Razão social da empresa")
    natureza_juridica = Column(String(4), nullable=True, index=True, comment="Código da natureza jurídica")
    qualificacao_responsavel = Column(String(2), nullable=True, comment="Código qualificação do responsável")
    capital_social = Column(String(20), nullable=True, comment="Capital social (formato: 0,00)")
    porte_empresa = Column(String(2), nullable=True, index=True, comment="Código do porte: 00=Não Informado, 01=Micro, 03=Pequeno, 05=Demais")
    ente_federativo_responsavel = Column(String, nullable=True, comment="Ente federativo responsável")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    estabelecimentos = relationship("Estabelecimento", back_populates="empresa")
    socios = relationship("Socio", back_populates="empresa")


class Estabelecimento(Base):
    """Estabelecimento model - Dados de matriz e filiais (endereços)"""
    
    __tablename__ = "estabelecimentos"
    
    __table_args__ = (
        Index('idx_estabelecimentos_cnpj_completo', 'cnpj_completo'),
        Index('idx_estabelecimentos_cnpj_basico', 'cnpj_basico'),
        Index('idx_estabelecimentos_uf_municipio', 'uf', 'municipio'),
        Index('idx_estabelecimentos_situacao', 'situacao_cadastral'),
        Index('idx_estabelecimentos_cnae_principal', 'cnae_fiscal_principal'),
        {'comment': 'Estabelecimentos (matriz e filiais) com endereços completos'}
    )
    
    id = Column(Integer, primary_key=True, index=True)
    cnpj_basico = Column(String(8), nullable=False, index=True, comment="CNPJ básico (liga com empresas)")
    cnpj_ordem = Column(String(4), nullable=False, comment="Ordem do estabelecimento")
    cnpj_dv = Column(String(2), nullable=False, comment="Dígito verificador")
    cnpj_completo = Column(String(14), unique=True, nullable=False, comment="CNPJ completo (básico+ordem+dv)")
    identificador_matriz_filial = Column(String(1), nullable=True, comment="1=Matriz, 2=Filial")
    nome_fantasia = Column(String, nullable=True, comment="Nome fantasia")
    situacao_cadastral = Column(String(2), nullable=True, index=True, comment="Código da situação cadastral")
    data_situacao_cadastral = Column(String(8), nullable=True, comment="Data situação (YYYYMMDD)")
    motivo_situacao_cadastral = Column(String(2), nullable=True, comment="Código do motivo")
    cidade_exterior = Column(String, nullable=True, comment="Nome da cidade no exterior")
    pais = Column(String(3), nullable=True, comment="Código do país")
    data_inicio_atividade = Column(String(8), nullable=True, comment="Data início (YYYYMMDD)")
    cnae_fiscal_principal = Column(String(7), nullable=True, index=True, comment="CNAE principal")
    cnae_fiscal_secundaria = Column(Text, nullable=True, comment="CNAEs secundários (separados por vírgula)")
    tipo_logradouro = Column(String, nullable=True, comment="Tipo: RUA, AVENIDA, etc")
    logradouro = Column(String, nullable=True, comment="Nome do logradouro")
    numero = Column(String, nullable=True, comment="Número")
    complemento = Column(String, nullable=True, comment="Complemento")
    bairro = Column(String, nullable=True, comment="Bairro")
    cep = Column(String(8), nullable=True, index=True, comment="CEP (8 dígitos)")
    uf = Column(String(2), nullable=True, index=True, comment="UF (sigla)")
    municipio = Column(String(4), nullable=True, index=True, comment="Código IBGE do município")
    ddd_1 = Column(String(4), nullable=True, comment="DDD telefone 1")
    telefone_1 = Column(String(8), nullable=True, comment="Telefone 1")
    ddd_2 = Column(String(4), nullable=True, comment="DDD telefone 2")
    telefone_2 = Column(String(8), nullable=True, comment="Telefone 2")
    ddd_fax = Column(String(4), nullable=True, comment="DDD fax")
    fax = Column(String(8), nullable=True, comment="Fax")
    email = Column(String, nullable=True, comment="E-mail")
    situacao_especial = Column(String, nullable=True, comment="Situação especial")
    data_situacao_especial = Column(String(8), nullable=True, comment="Data situação especial (YYYYMMDD)")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    empresa = relationship("Empresa", back_populates="estabelecimentos")


class Socio(Base):
    """Socio model - Quadro societário (sócios e administradores)"""
    
    __tablename__ = "socios"
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    empresa = relationship("Empresa", back_populates="socios")
    
    # Index for searches
    __table_args__ = (
        Index('idx_socio_nome', 'nome_socio'),
        Index('idx_socio_cpf_cnpj', 'cpf_cnpj_socio'),
    )
