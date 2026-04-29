from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root regardless of where uvicorn is run from
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# Your actual database credentials
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(DATABASE_URL)

# Session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)