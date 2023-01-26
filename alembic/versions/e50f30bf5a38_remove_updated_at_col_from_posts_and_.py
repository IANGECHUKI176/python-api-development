"""remove updated_at col from posts and add published

Revision ID: e50f30bf5a38
Revises: a80dd0baa382
Create Date: 2023-01-26 17:51:03.969091

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e50f30bf5a38'
down_revision = 'a80dd0baa382'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('posts', 'updated_at')
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'updated_at')
    op.drop_column('posts','created_at')
    pass
