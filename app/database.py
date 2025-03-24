from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# Create database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base model for ORM
Base = declarative_base()

def create_tables():
    """Create tables in the database."""
    from app.models import User, Post, Comment
    Base.metadata.create_all(bind=engine)
