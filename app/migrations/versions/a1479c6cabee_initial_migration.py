"""Initial migration

Revision ID: a1479c6cabee
Revises: 43392c881aa1
Create Date: 2024-10-20 18:12:41.974529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1479c6cabee'
down_revision: Union[str, None] = '43392c881aa1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(), nullable=True))
    op.drop_column('users', 'age')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('age', sa.INTEGER(), nullable=True))
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
