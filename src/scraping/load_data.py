import os
import json
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)
cur = conn.cursor()

raw_dir = "data/raw/telegram_messages/"

for date_folder in os.listdir(raw_dir):
    folder_path = os.path.join(raw_dir, date_folder)
    if os.path.isdir(folder_path):
        for file in os.listdir(folder_path):
            if file.endswith(".json"):
                channel = file.replace(".json", "")
                file_path = os.path.join(folder_path, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        messages = json.load(f)
                        for msg in messages:
                            cur.execute("""
                                INSERT INTO raw.telegram_messages (id, channel, message_json)
                                VALUES (%s, %s, %s)
                                ON CONFLICT (id) DO NOTHING;
                            """, (
                                msg.get('id'),
                                channel,
                                json.dumps(msg)
                            ))
                    except Exception as e:
                        print(f"Error loading {file_path}: {e}")

conn.commit()
cur.close()
conn.close()
print("Raw Telegram messages loaded into PostgreSQL.")