"""Create Vacancy Table

Revision ID: 426f7f82ce2b
Revises: 22d3d594b8cb
Create Date: 2024-10-18 23:21:07.794937

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '426f7f82ce2b'
down_revision: Union[str, None] = '22d3d594b8cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создаём таблицу vacancys
    op.create_table(
        'vacancys',
        sa.Column('id', sa.UUID(as_uuid=True), primary_key=True, index=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column('vacancy_title', sa.String(), nullable=False),
        sa.Column('work_category', sa.String(), nullable=False),
        sa.Column('experience', sa.Integer(), nullable=False),
        sa.Column('key_skils', sa.String(), nullable=False),
        sa.Column('is_exist', sa.Boolean(), nullable=False, server_default=sa.sql.expression.true()),
        sa.Column('location', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('conditions', sa.String(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('date_of_pub', sa.DateTime(), nullable=False, default=datetime.utcnow),
    )

def downgrade():
    # Удаляем таблицу vacancys
    op.drop_table('vacancys')