# File Path: src/yolo/image_analyzer.py
# Date: 10 July 2025
# Developed by: Addisu Taye Dadi
# Purpose: Detect objects in scraped images using YOLOv8.
# Key Features:
# - Uses YOLOv8 to detect objects in downloaded Telegram images.
# - Stores results in PostgreSQL table: raw.fct_image_detections
# - Automatically creates the table if it doesn't exist
# - Logs confidence scores and class names for analysis
# - Added progress tracking, counters, and console output

from ultralytics import YOLO
import os
import logging
from dotenv import load_dotenv
import psycopg2
from datetime import datetime

# Load environment variables
load_dotenv()

# Set up logging to file
logging.basicConfig(
    filename='image_analysis.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Console progress helpers
def log_info(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    logging.info(message)

def log_error(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ERROR: {message}")
    logging.error(message)

# Define SQL for creating detection table
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS raw.fct_image_detections (
    detection_id SERIAL PRIMARY KEY,
    message_id TEXT NOT NULL,
    detected_object_class TEXT NOT NULL,
    confidence_score FLOAT NOT NULL,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Initialize YOLO model
try:
    log_info("⏳ Loading YOLOv8 model...")
    model = YOLO("yolov8s.pt")  # Will auto-download if not found
    log_info("✅ YOLOv8 model loaded successfully.")

except Exception as e:
    log_error(f"Failed to load YOLO model: {e}")
    raise

# Image directory path
image_dir = "data/raw/images/"

# PostgreSQL connection
try:
    log_info("🔌 Connecting to PostgreSQL database...")
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    log_info("✅ Connected to PostgreSQL")

    # Create table if not exists
    log_info("🗃️ Ensuring detection table exists...")
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    log_info("✅ Table 'raw.fct_image_detections' created or already exists.")

    # Analyze images
    total_images = 0
    total_detections = 0

    for folder in os.listdir(image_dir):
        channel_dir = os.path.join(image_dir, folder)
        if os.path.isdir(channel_dir):
            log_info(f"🖼️ Processing channel: {folder}")

            image_files = [f for f in os.listdir(channel_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            total_images += len(image_files)

            for img_file in image_files:
                img_path = os.path.join(channel_dir, img_file)
                log_info(f"🔍 Analyzing image: {img_file} ({folder})")

                try:
                    results = model(img_path)

                    for r in results:
                        detections = r.boxes
                        total_detections += len(detections)

                        for box in detections:
                            class_id = box.cls.item()
                            class_name = model.names[class_id]  # Map ID to label name
                            confidence = box.conf.item()
                            msg_id = img_file.split('.')[0]

                            cur.execute("""
                                INSERT INTO raw.fct_image_detections 
                                (message_id, detected_object_class, confidence_score)
                                VALUES (%s, %s, %s)
                            """, (msg_id, class_name, confidence))

                    log_info(f"✅ Detected {len(detections)} objects in {img_file}")
                except Exception as img_error:
                    log_error(f"Error analyzing image {img_path}: {img_error}")

    # Commit all inserts
    conn.commit()
    log_info(f"📊 Total images processed: {total_images}")
    log_info(f"🎯 Total object detections recorded: {total_detections}")
    log_info("📦 Image analysis completed and data committed to database.")

except Exception as e:
    log_error(f"Pipeline failed: {e}")
    conn.rollback()
    log_info("❌ Transaction rolled back due to error.")
finally:
    cur.close()
    conn.close()
    log_info("🔌 Connection to PostgreSQL closed.")