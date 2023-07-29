"""add possible policy updates field

Revision ID: 0e0532e88e44
Revises: 0f4c5a23b16f
Create Date: 2023-07-29 15:44:39.031502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0e0532e88e44"
down_revision = "0f4c5a23b16f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "gplay_app", sa.Column("possible_policy_updates", sa.String(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("gplay_app", "possible_policy_updates")
    # ### end Alembic commands ###
