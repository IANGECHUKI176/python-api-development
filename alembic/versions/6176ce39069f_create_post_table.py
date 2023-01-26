"""create post table

Revision ID: 6176ce39069f
Revises: 
Create Date: 2023-01-26 16:09:42.001245

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6176ce39069f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
