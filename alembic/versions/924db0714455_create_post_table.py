"""create post table

Revision ID: 924db0714455
Revises: 
Create Date: 2022-01-23 16:56:43.857373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '924db0714455'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts",
    sa.Column("id", sa.Integer, primary_key=True, index=True, nullable=False),
    sa.Column("title", sa.String(255), nullable=False),
    sa.Column("content", sa.String(500), nullable=False),
    sa.Column("published", sa.Boolean, nullable=False, server_default="True"),
    sa.Column("rating", sa.Integer, nullable=False, server_default="0"),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
    sa.Column("updated_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()"))
    )


def downgrade():
    op.drop_table("posts")
