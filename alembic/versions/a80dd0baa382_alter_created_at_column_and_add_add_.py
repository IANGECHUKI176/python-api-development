"""alter created at column  and add add foreign key

Revision ID: a80dd0baa382
Revises: 0627643d74de
Create Date: 2023-01-26 17:35:34.766363

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a80dd0baa382'
down_revision = '0627643d74de'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('posts', 'created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'],
                          remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts')
    op.drop_column('posts', 'owner_id')

    pass
