# File Path: src/scraping/load_data.py
# Date: 10 July 2025
# Developed by: Addisu Taye Dadi
# Purpose: Load raw Telegram JSON data into PostgreSQL raw schema.
# Key Features:
# - Reads partitioned JSON files from data/raw/
# - Ensures the raw.telegram_messages table exists
# - Inserts raw message data into PostgreSQL table: raw.telegram_messages
# - Uses ON CONFLICT to avoid duplicate inserts
# - Logs progress and errors

import os
import json
import logging
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    filename='loading.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# PostgreSQL connection
try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    logging.info("Connected to PostgreSQL")

except Exception as e:
    logging.error(f"Failed to connect to PostgreSQL: {e}")
    raise

def create_schema_and_table():
    """Ensures the raw schema and telegram_messages table exist."""
    try:
        # Create schema if not exists
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")

        # Create table if not exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw.telegram_messages (
                id BIGINT PRIMARY KEY,
                channel TEXT NOT NULL,
                message_json JSONB NOT NULL,
                extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        logging.info("Schema and table created or already exist.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error creating schema/table: {e}")
        raise

try:
    # Ensure schema and table exist before loading
    create_schema_and_table()

    raw_dir = "data/raw/telegram_messages/"

    # Traverse directory and load each JSON file
    for date_folder in os.listdir(raw_dir):
        folder_path = os.path.join(raw_dir, date_folder)
        
        if os.path.isdir(folder_path):
            logging.info(f"Processing folder: {folder_path}")
            
            for file in os.listdir(folder_path):
                if file.endswith(".json"):
                    channel = file.replace(".json", "")
                    file_path = os.path.join(folder_path, file)
                    
                    logging.info(f"Loading file: {file_path}")
                    
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            messages = json.load(f)

                            for msg in messages:
                                message_id = msg.get('id')
                                if not message_id:
                                    logging.warning(f"Message missing 'id' field in {file_path}")
                                    continue

                                cur.execute("""
                                    INSERT INTO raw.telegram_messages (id, channel, message_json)
                                    VALUES (%s, %s, %s)
                                    ON CONFLICT (id) DO NOTHING;
                                """, (
                                    message_id,
                                    channel,
                                    json.dumps(msg)
                                ))

                            logging.info(f"Loaded {len(messages)} messages from {file}")

                    except json.JSONDecodeError as je:
                        logging.error(f"JSON decode error in {file_path}: {je}")
                    except Exception as e:
                        logging.error(f"Unexpected error loading {file_path}: {e}")

    conn.commit()
    logging.info("All data loaded successfully.")

except Exception as e:
    conn.rollback()
    logging.error(f"Transaction failed: {e}")
finally:
    cur.close()
    conn.close()
    print("Raw Telegram messages loaded into PostgreSQL.")