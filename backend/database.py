from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get DATABASE_URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")
elif DATABASE_URL.startswith("postgres://"):
    # Handle Railway's Postgres URL format if present
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Enhanced logging
host = DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else 'unknown'
db_name = DATABASE_URL.split('/')[-1] if '/' in DATABASE_URL else 'unknown'
print(f"\n=== Database Connection Info ===")
print(f"Host: {host}")
print(f"Database: {db_name}")
print("============================\n")

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