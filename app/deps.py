from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Generator
from .database import SessionLocal

# Dependency to get the database session
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()