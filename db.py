import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_connection():
    """Create and return a database connection"""
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def init_database():
    """Initialize database by running schema.sql"""
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()

        # Read and execute schema.sql
        with open("schema.sql", "r") as f:
            schema = f.read()

        cursor.execute(schema)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database initialized successfully!")
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False


init_database()
