"""create auxiliary tables

Revision ID: 20251122_1630
Revises: 
Create Date: 2025-11-22 16:30:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251122_1630'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create CNAEs table
    op.create_table(
        'cnaes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('codigo', sa.String(length=7), nullable=False),
        sa.Column('descricao', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_cnaes_codigo', 'cnaes', ['codigo'], unique=True)
    op.create_index('ix_cnaes_id', 'cnaes', ['id'], unique=False)
    
    # Create Municipios table
    op.create_table(
        'municipios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('codigo', sa.String(length=4), nullable=False),
        sa.Column('descricao', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_municipios_codigo', 'municipios', ['codigo'], unique=True)
    op.create_index('ix_municipios_id', 'municipios', ['id'], unique=False)
    
    # Create Naturezas table
    op.create_table(
        'naturezas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('codigo', sa.String(length=4), nullable=False),
        sa.Column('descricao', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_naturezas_codigo', 'naturezas', ['codigo'], unique=True)
    op.create_index('ix_naturezas_id', 'naturezas', ['id'], unique=False)
    
    # Create Paises table
    op.create_table(
        'paises',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('codigo', sa.String(length=3), nullable=False),
        sa.Column('descricao', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_paises_codigo', 'paises', ['codigo'], unique=True)
    op.create_index('ix_paises_id', 'paises', ['id'], unique=False)
    
    # Create Qualificacoes table
    op.create_table(
        'qualificacoes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('codigo', sa.String(length=2), nullable=False),
        sa.Column('descricao', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_qualificacoes_codigo', 'qualificacoes', ['codigo'], unique=True)
    op.create_index('ix_qualificacoes_id', 'qualificacoes', ['id'], unique=False)
    
    # Create Motivos table
    op.create_table(
        'motivos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('codigo', sa.String(length=2), nullable=False),
        sa.Column('descricao', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_motivos_codigo', 'motivos', ['codigo'], unique=True)
    op.create_index('ix_motivos_id', 'motivos', ['id'], unique=False)
    
    # Create Simples table
    op.create_table(
        'simples',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cnpj_basico', sa.String(length=8), nullable=False),
        sa.Column('opcao_simples', sa.String(length=1), nullable=True),
        sa.Column('data_opcao_simples', sa.String(length=8), nullable=True),
        sa.Column('data_exclusao_simples', sa.String(length=8), nullable=True),
        sa.Column('opcao_mei', sa.String(length=1), nullable=True),
        sa.Column('data_opcao_mei', sa.String(length=8), nullable=True),
        sa.Column('data_exclusao_mei', sa.String(length=8), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_simples_cnpj_basico', 'simples', ['cnpj_basico'], unique=True)
    op.create_index('ix_simples_id', 'simples', ['id'], unique=False)


def downgrade() -> None:
    op.drop_table('simples')
    op.drop_table('motivos')
    op.drop_table('qualificacoes')
    op.drop_table('paises')
    op.drop_table('naturezas')
    op.drop_table('municipios')
    op.drop_table('cnaes')
