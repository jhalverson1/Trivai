from sqlalchemy import create_engine, text
from models import Base
import os

def verify_database():
    try:
        # Print tables from metadata
        print("Tables in metadata:", Base.metadata.tables.keys())

        # Check actual database
        db_url = os.getenv('DATABASE_URL')
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public'"))
            tables = [row[0] for row in result]
            print('Actual tables in database:', tables)
    except Exception as e:
        print(f"Error verifying database: {e}")

if __name__ == "__main__":
    verify_database() 