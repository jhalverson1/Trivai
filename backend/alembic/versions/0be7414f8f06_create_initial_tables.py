"""create initial tables

Revision ID: 0be7414f8f06
Revises: 
Create Date: 2024-12-20 21:09:29.209386

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '0be7414f8f06'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create alembic_version table first
    op.execute("""
        CREATE TABLE IF NOT EXISTS alembic_version (
            version_num VARCHAR(32) NOT NULL,
            CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
        )
    """)

    # Drop existing tables and types
    op.execute('DROP TABLE IF EXISTS questions CASCADE')
    op.execute('DROP TABLE IF EXISTS games CASCADE')
    op.execute('DROP TABLE IF EXISTS difficulties CASCADE')
    op.execute('DROP TYPE IF EXISTS gamestatus')

    # Create difficulties table first
    op.create_table('difficulties',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
        sa.Column('description', sa.String())
    )

    # Seed difficulties data
    difficulties_table = sa.table('difficulties',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String),
        sa.column('description', sa.String)
    )
    
    op.bulk_insert(difficulties_table, [
        {'id': 1, 'name': 'Beginner', 'description': 'Basic knowledge questions suitable for beginners'},
        {'id': 2, 'name': 'Easy', 'description': 'Simple questions with straightforward answers'},
        {'id': 3, 'name': 'Medium', 'description': 'Moderate difficulty requiring good general knowledge'},
        {'id': 4, 'name': 'Hard', 'description': 'Challenging questions for knowledgeable players'},
        {'id': 5, 'name': 'Expert', 'description': 'Very difficult questions for trivia experts'}
    ])

    # Create games table
    op.create_table('games',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('category', sa.String()),
        sa.Column('number_of_questions', sa.Integer(), nullable=False),
        sa.Column('difficulty_id', sa.Integer(), nullable=False),
        sa.Column('current_question_index', sa.Integer(), server_default='0'),
        sa.Column('score', sa.Integer(), server_default='0'),
        sa.Column('status', sa.Enum('pending', 'in_progress', 'completed', name='gamestatus')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.text('now()')),
        sa.ForeignKeyConstraint(['difficulty_id'], ['difficulties.id'])
    )

    # Create questions table
    op.create_table('questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.String(), nullable=False),
        sa.Column('correct_answer', sa.String(), nullable=False),
        sa.Column('options', sa.String(), nullable=False),
        sa.Column('difficulty_id', sa.Integer(), nullable=False),
        sa.Column('game_id', sa.Integer()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['difficulty_id'], ['difficulties.id']),
        sa.ForeignKeyConstraint(['game_id'], ['games.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questions_id'), 'questions', ['id'], unique=False)
    op.create_index(op.f('ix_games_id'), 'games', ['id'], unique=False)

def downgrade() -> None:
    op.drop_index(op.f('ix_questions_id'), table_name='questions')
    op.drop_index(op.f('ix_games_id'), table_name='games')
    op.drop_table('questions')
    op.drop_table('games')
    op.drop_table('difficulties')
    op.execute('DROP TYPE gamestatus') 