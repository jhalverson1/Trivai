from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get DATABASE_URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# If no DATABASE_URL is provided, check if we're running in Docker
if not DATABASE_URL:
    # Default for local Docker development
    DATABASE_URL = "postgresql://postgres:postgres@db:5432/trivai"
    print("No DATABASE_URL found, using Docker default")
elif DATABASE_URL.startswith("postgres://"):
    # Handle Railway's Postgres URL format if present
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"Connecting to database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'local'}")  # Safe logging

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 