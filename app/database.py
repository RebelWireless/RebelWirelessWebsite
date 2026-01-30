# app/database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base  # updated import
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

import os

# Example: postgres://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/rebelwireless")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = Base.metadata

# -----------------------
# Dependency for FastAPI
# -----------------------
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
