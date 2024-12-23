from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
from models import Base

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Get the database URL from environment
def get_url():
    db_url = os.getenv("DATABASE_URL")
    print("\n=== Alembic Database Connection Info ===")
    print(f"Original URL: {db_url}")
    
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        print(f"Modified URL: {db_url}")
    
    host = db_url.split('@')[1].split('/')[0] if '@' in db_url else 'unknown'
    db_name = db_url.split('/')[-1] if '/' in db_url else 'unknown'
    print(f"Host: {host}")
    print(f"Database: {db_name}")
    print("=====================================\n")
    return db_url

# Set the target metadata
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    # Get the URL first
    url = get_url()
    
    # Create a configuration with the URL
    configuration = {
        'sqlalchemy.url': url,
        'script_location': 'alembic'
    }
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
