# File Path: src/api/database.py
# Date: July 10, 2025
# Developed by: Addisu Taye Dadi
# Purpose: Set up database connection engine
# Key Features:
# - Uses environment variables for secure credentials
# - Returns SQLAlchemy engine for querying dbt models

from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    db_url = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    return create_engine(db_url)