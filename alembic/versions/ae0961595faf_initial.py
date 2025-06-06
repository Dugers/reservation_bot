"""Initial

Revision ID: ae0961595faf
Revises: 
Create Date: 2025-05-22 22:28:03.639126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ae0961595faf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=16), nullable=False),
    sa.Column('short_description', sqlmodel.sql.sqltypes.AutoString(length=16), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reservation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_tg_id', sa.Integer(), nullable=False),
    sa.Column('start_datetime', sa.DateTime(), nullable=False),
    sa.Column('end_datetime', sa.DateTime(), nullable=False),
    sa.Column('table_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['table_id'], ['table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservation')
    op.drop_table('table')
    # ### end Alembic commands ###
