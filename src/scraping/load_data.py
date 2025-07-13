import os
import json
import psycopg2
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

print("🚀 Starting Telegram message loader...")

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    print("✅ Connected to PostgreSQL.")
except Exception as conn_err:
    print(f"❌ Failed to connect to the database: {conn_err}")
    exit()

# Set root directory
raw_dir = "data/raw/telegram_messages/"
if not os.path.exists(raw_dir):
    print(f"❌ Directory not found: {raw_dir}")
    exit()

inserted = 0
skipped = 0
total_files = 0

# Traverse folder structure
for date_folder in os.listdir(raw_dir):
    folder_path = os.path.join(raw_dir, date_folder)
    if os.path.isdir(folder_path):
        print(f"\n📁 Scanning folder: {folder_path}")
        for file in os.listdir(folder_path):
            if file.endswith(".json"):
                total_files += 1
                channel = file.replace(".json", "")
                file_path = os.path.join(folder_path, file)
                print(f"📄 Processing file: {file_path}")

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        messages = json.load(f)
                        print(f"   → Found {len(messages)} messages.")

                        for msg in messages:
                            msg_id = msg.get("id")
                            if not msg_id:
                                print(f"⚠️ Skipping message with no ID in {file}")
                                skipped += 1
                                continue

                            try:
                                cur.execute("""
                                    INSERT INTO telegram_messages (id, channel, message_json)
                                    VALUES (%s, %s, %s)
                                    ON CONFLICT (id) DO NOTHING;
                                """, (
                                    msg_id,
                                    channel,
                                    json.dumps(msg)
                                ))
                                inserted += 1
                            except Exception as insert_err:
                                print(f"❌ Insert error for msg ID {msg_id}: {insert_err}")
                                skipped += 1

                except Exception as file_err:
                    print(f"❌ Error reading file {file_path}: {file_err}")
                    continue

# Commit and close
conn.commit()
print(f"\n✅ Done. Processed {total_files} file(s).")
print(f"📦 Messages inserted: {inserted}")
print(f"⛔ Messages skipped: {skipped}")

# Post-insert verification
try:
    cur.execute("SELECT COUNT(*) FROM telegram_messages;")
    total_rows = cur.fetchone()[0]
    print(f"\n📊 Total rows in 'telegram_messages': {total_rows}")

    cur.execute("SELECT id, channel FROM telegram_messages ORDER BY id DESC LIMIT 5;")
    print("🔍 Sample inserted rows:")
    for row in cur.fetchall():
        print(f"   → ID: {row[0]}, Channel: {row[1]}")

except Exception as query_err:
    print(f"❌ Verification query failed: {query_err}")

# Cleanup
cur.close()
conn.close()
print("🔒 PostgreSQL connection closed.")
