import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection string format:
# postgresql://[user]:[password]@[host]:[port]/[dbname]
# Replace these values with your Google Cloud PostgreSQL credentials
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@34.70.227.62:5432")

# For local development, you might use Cloud SQL Proxy with this URL instead:
# DATABASE_URL_LOCAL = "postgresql://username:password@localhost:5432/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


