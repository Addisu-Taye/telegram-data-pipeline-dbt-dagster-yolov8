# File Path: src/api/main.py
# Date: 10 July 2025
# Developed by: Addisu Taye Dadi
# Purpose: Main FastAPI application to expose analytical insights from dbt models.
# Key Features:
# - Exposes endpoints like /api/reports/top-products
# - Uses Pydantic schemas for request/response validation
# - Connects to PostgreSQL using environment variables

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Telegram Analytics API",
    description="An API to access insights derived from Ethiopian medical Telegram channels",
    version="1.0"
)

# Add CORS middleware to allow all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PostgreSQL connection using environment variables
try:
    db_url = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    engine = create_engine(db_url)
    logger.info("✅ Successfully connected to PostgreSQL")
except Exception as e:
    logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
    raise

# Optional: Define a base model for structured responses
class ProductReportItem(BaseModel):
    product: str
    count: int

class ChannelActivityItem(BaseModel):
    year: int
    month: str
    message_count: int

class MessageSearchResult(BaseModel):
    message_id: int
    text: str
    date: str | None
    channel: str

# Sample endpoint to test if API is running
@app.get("/")
def root():
    return {
        "status": "Online",
        "message": "Welcome to the Telegram analytics API",
        "version": "1.0",
        "endpoints": [
            "/api/reports/top-products?limit=10",
            "/api/channels/{channel_name}/activity",
            "/api/search/messages?query=paracetamol"
        ]
    }

# Endpoint: Get Top Products Mentioned in Messages
@app.get("/api/reports/top-products", response_model=list[ProductReportItem])
def top_products(limit: int = 10):
    """
    Returns the most frequently mentioned products or drugs in Telegram messages.
    Example: paracetamol, ibuprofen, etc.
    """
    try:
        result = engine.execute(f"""
            SELECT message_text, COUNT(*) AS count
            FROM fct_messages
            WHERE message_text ILIKE '%paracetamol%' OR message_text ILIKE '%ibuprofen%'
            GROUP BY message_text
            ORDER BY count DESC
            LIMIT {limit}
        """).fetchall()
        logger.info(f"📊 Fetched top {limit} products")
        return [{"product": r[0], "count": r[1]} for r in result]
    except Exception as e:
        logger.error(f"🚨 Error fetching top products: {e}")
        return {"error": str(e)}

# Endpoint: Get Posting Activity for a Specific Channel
@app.get("/api/channels/{channel_name}/activity", response_model=list[ChannelActivityItem])
def channel_activity(channel_name: str):
    """
    Returns daily/weekly/monthly activity for a specific Telegram channel.
    Used to analyze posting trends over time.
    """
    try:
        result = engine.execute(f"""
            SELECT d.year, d.month_name, COUNT(*) AS message_count
            FROM fct_messages m
            JOIN dim_channels c ON m.channel_id = c.channel_id
            JOIN dim_dates d ON DATE(m.message_date) = d.date
            WHERE c.channel_name = '{channel_name}'
            GROUP BY d.year, d.month_name
            ORDER BY d.date DESC
        """).fetchall()
        logger.info(f"📈 Fetched activity data for channel: {channel_name}")
        return [{"year": r[0], "month": r[1], "message_count": r[2]} for r in result]
    except Exception as e:
        logger.error(f"🚨 Error fetching activity for {channel_name}: {e}")
        return {"error": str(e)}

# Endpoint: Search for Messages Containing a Keyword
@app.get("/api/search/messages")
def search_messages(query: str):
    """
    Search for messages containing a specific keyword (e.g., drug name).
    Useful for monitoring availability or price changes across channels.
    """
    try:
        result = engine.execute(f"""
            SELECT m.message_id, m.message_text, m.message_date, c.channel_name
            FROM fct_messages m
            JOIN dim_channels c ON m.channel_id = c.channel_id
            WHERE m.message_text ILIKE '%{query}%'
            ORDER BY m.message_date DESC
        """).fetchall()
        logger.info(f"🔍 Searched for '{query}' in messages")
        return [{
            "message_id": r[0],
            "text": r[1],
            "date": r[2],
            "channel": r[3]
        } for r in result]
    except Exception as e:
        logger.error(f"🚨 Error searching messages: {e}")
        return {"error": str(e)}