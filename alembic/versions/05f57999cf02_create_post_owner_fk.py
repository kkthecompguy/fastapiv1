"""create post owner fk

Revision ID: 05f57999cf02
Revises: 4d8fb7931236
Create Date: 2022-01-23 20:56:31.748572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05f57999cf02'
down_revision = '4d8fb7931236'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer,  nullable=False)
    )
    op.create_foreign_key(
        "post_users_fkey",
        source_table="posts",
        referent_table="users",
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint("post_users_fkey")
    op.drop_column("posts", "owner_id")
