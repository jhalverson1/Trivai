"""add categories table

Revision ID: 2023_12_add_categories
Revises: 0be7414f8f06
Create Date: 2023-12-20 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '2023_12_add_categories'
down_revision = '0be7414f8f06'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Drop old category column from games
    op.execute("ALTER TABLE games DROP COLUMN IF EXISTS category")
    
    # Create categories table
    op.execute("""
        CREATE TABLE categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL UNIQUE,
            search_count INTEGER DEFAULT 1,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE
        )
    """)

    # Add category_id to games and questions tables
    op.execute("""
        ALTER TABLE games 
        ADD COLUMN category_id INTEGER REFERENCES categories(id)
    """)

    op.execute("""
        ALTER TABLE questions 
        ADD COLUMN category_id INTEGER REFERENCES categories(id)
    """)

def downgrade() -> None:
    op.execute("ALTER TABLE questions DROP COLUMN category_id")
    op.execute("ALTER TABLE games DROP COLUMN category_id")
    op.execute("DROP TABLE categories")
    op.execute("ALTER TABLE games ADD COLUMN category VARCHAR")