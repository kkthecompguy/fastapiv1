"""create votes table

Revision ID: 4d8fb7931236
Revises: f146aac69ec4
Create Date: 2022-01-23 20:40:12.527865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d8fb7931236'
down_revision = 'f146aac69ec4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "votes",
        sa.Column("user_id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("post_id", sa.Integer, nullable=False, primary_key=True),
    )
    op.create_foreign_key("votes_users_fkey", source_table="votes", referent_table="users", local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    op.create_foreign_key("votes_posts_fkey", source_table="votes", referent_table="posts", local_cols=['post_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade():
    op.drop_constraint("votes_users_fkey", table_name="votes")
    op.drop_constraint("votes_posts_fkey", table_name="votes")
    op.drop_table("votes")
