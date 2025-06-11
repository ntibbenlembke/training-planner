from .database import engine, Base
from . import models

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("Database tables created!") 