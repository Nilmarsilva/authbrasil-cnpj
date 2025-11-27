"""create etl_status table

Revision ID: 20251127_0730
Revises: 9b0693a6cde3
Create Date: 2025-11-27 07:30:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20251127_0730'
down_revision = '9b0693a6cde3'  # Version atual do banco na VPS
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create etl_status table
    op.create_table(
        'etl_status',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('job_id', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('current_step', sa.String(), nullable=True),
        sa.Column('current_file', sa.String(), nullable=True),
        sa.Column('current_table', sa.String(), nullable=True),
        sa.Column('progress_percent', sa.Float(), nullable=True),
        sa.Column('files_processed', sa.Integer(), nullable=True),
        sa.Column('files_total', sa.Integer(), nullable=True),
        sa.Column('records_imported', sa.Integer(), nullable=True),
        sa.Column('disk_free_gb', sa.Float(), nullable=True),
        sa.Column('disk_used_gb', sa.Float(), nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('elapsed_seconds', sa.Integer(), nullable=True),
        sa.Column('estimated_remaining_seconds', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.String(), nullable=True),
        sa.Column('warnings', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_etl_status_id', 'etl_status', ['id'], unique=False)
    op.create_index('ix_etl_status_job_id', 'etl_status', ['job_id'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_etl_status_job_id', table_name='etl_status')
    op.drop_index('ix_etl_status_id', table_name='etl_status')
    op.drop_table('etl_status')
