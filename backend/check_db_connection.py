from sqlalchemy import create_engine, text
from database.database import DATABASE_URL

def check_db_connection():
    """Test connection to the PostgreSQL database"""
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Try to connect and execute a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            row = result.fetchone()
            if row[0] == 1:
                print("✅ Database connection successful!")
                return True
            else:
                print("❌ Database connection failed: Unexpected result from test query")
                return False
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    check_db_connection() 