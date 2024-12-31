from sqlalchemy import create_engine
from app.database import Base
from app.models import Customer, Account, Document
import os
from dotenv import load_dotenv

load_dotenv()

def create_tables():
    try:
        # Get database URL from environment variable
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not set")

        # Create engine
        engine = create_engine(database_url)

        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")

    except Exception as e:
        print(f"Error creating tables: {str(e)}")

if __name__ == "__main__":
    create_tables()