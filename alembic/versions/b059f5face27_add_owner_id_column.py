"""add owner_id column

Revision ID: b059f5face27
Revises: 6176ce39069f
Create Date: 2023-01-26 16:36:19.916650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b059f5face27'
down_revision = '6176ce39069f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'owner_id')
    pass
