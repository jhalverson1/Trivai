"""create questions table

Revision ID: 0be7414f8f06
Revises: 
Create Date: 2024-12-20 21:09:29.209386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0be7414f8f06'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.String(), nullable=False),
        sa.Column('correct_answer', sa.String(), nullable=False),
        sa.Column('options', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questions_id'), 'questions', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_questions_id'), table_name='questions')
    op.drop_table('questions')
