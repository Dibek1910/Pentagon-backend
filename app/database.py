from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

try:
    # Create engine with logging
    engine = create_engine(
        DATABASE_URL,
        echo=True  # This will log all SQL statements
    )
    
    # Test connection
    with engine.connect() as connection:
        logger.info("Successfully connected to the database!")

except Exception as e:
    logger.error(f"Error connecting to database: {str(e)}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()