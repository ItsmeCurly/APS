"""add app category

Revision ID: f0b2ebe9e08a
Revises: 56c45d1626e1
Create Date: 2023-06-11 12:19:24.915288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f0b2ebe9e08a"
down_revision = "56c45d1626e1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("gplay_app", sa.Column("app_category", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("gplay_app", "app_category")
    # ### end Alembic commands ###
