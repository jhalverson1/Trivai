from sqlalchemy import create_engine, text, inspect
from models import Base
import os

def verify_database():
    try:
        print("Tables in metadata:", Base.metadata.tables.keys())
        
        db_url = os.getenv('DATABASE_URL')
        engine = create_engine(db_url)
        inspector = inspect(engine)
        
        print("\nActual database structure:")
        for table_name in inspector.get_table_names():
            print(f"\nTable: {table_name}")
            for column in inspector.get_columns(table_name):
                print(f"  - {column['name']}: {column['type']}")
            
            print("  Foreign Keys:")
            for fk in inspector.get_foreign_keys(table_name):
                print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
                
    except Exception as e:
        print(f"Error verifying database: {e}")

if __name__ == "__main__":
    verify_database() 