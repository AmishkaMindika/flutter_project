from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# MySQL Database URL (Update with your credentials)
DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/mydatabase"

# Create Engine
engine = create_engine(DATABASE_URL, echo=True)

# Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Class for Models
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
