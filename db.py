import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

connection_str = os.getenv("DATABASE_URL")

print(connection_str)
