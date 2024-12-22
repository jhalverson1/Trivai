from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Create difficulties table
    op.create_table(
        'difficulties',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
        sa.Column('description', sa.String())
    )

    # Insert default difficulties
    op.execute("""
        INSERT INTO difficulties (id, name, description) VALUES
        (1, 'Beginner', 'Very easy questions'),
        (2, 'Easy', 'Basic knowledge questions'),
        (3, 'Medium', 'Moderate difficulty questions'),
        (4, 'Hard', 'Challenging questions'),
        (5, 'Expert', 'Very difficult questions')
    """)

def downgrade():
    op.drop_table('difficulties') 