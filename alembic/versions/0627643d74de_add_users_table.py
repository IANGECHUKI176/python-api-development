"""add users table

Revision ID: 0627643d74de
Revises: b059f5face27
Create Date: 2023-01-26 16:46:10.203167

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0627643d74de'
down_revision = 'b059f5face27'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    pass


def downgrade() -> None:
    pass
