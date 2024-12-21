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
    try:
        # Drop existing tables and types first
        op.execute('DROP TABLE IF EXISTS questions CASCADE')
        op.execute('DROP TABLE IF EXISTS games CASCADE')
        op.execute('DROP TABLE IF EXISTS difficulties CASCADE')
        op.execute('DROP TYPE IF EXISTS gamestatus')
        
        # Create difficulties table
        op.execute("""
            CREATE TABLE difficulties (
                id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL UNIQUE,
                description VARCHAR
            )
        """)
        
        # Create games table with enum
        op.execute("""
            CREATE TYPE gamestatus AS ENUM ('pending', 'in_progress', 'completed');
            CREATE TABLE games (
                id SERIAL PRIMARY KEY,
                category VARCHAR,
                number_of_questions INTEGER NOT NULL,
                difficulty_id INTEGER NOT NULL REFERENCES difficulties(id),
                current_question_index INTEGER DEFAULT 0,
                score INTEGER DEFAULT 0,
                status gamestatus DEFAULT 'pending',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
                updated_at TIMESTAMP WITH TIME ZONE
            )
        """)
        
        # Create questions table
        op.execute("""
            CREATE TABLE questions (
                id SERIAL PRIMARY KEY,
                question_text VARCHAR NOT NULL,
                correct_answer VARCHAR NOT NULL,
                options VARCHAR NOT NULL,
                difficulty_id INTEGER NOT NULL REFERENCES difficulties(id),
                game_id INTEGER REFERENCES games(id),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            )
        """)
        
        # Seed difficulties
        op.execute("""
            INSERT INTO difficulties (id, name, description) VALUES
            (1, 'Beginner', 'Basic knowledge questions suitable for beginners'),
            (2, 'Easy', 'Simple questions with straightforward answers'),
            (3, 'Medium', 'Moderate difficulty requiring good general knowledge'),
            (4, 'Hard', 'Challenging questions for knowledgeable players'),
            (5, 'Expert', 'Very difficult questions for trivia experts')
        """)
        
    except Exception as e:
        print(f"Error in migration: {str(e)}")
        raise

def downgrade() -> None:
    op.drop_index(op.f('ix_questions_id'), table_name='questions')
    op.drop_index(op.f('ix_games_id'), table_name='games')
    op.drop_table('questions')
    op.drop_table('games')
    op.drop_table('difficulties')
    op.execute('DROP TYPE gamestatus') 