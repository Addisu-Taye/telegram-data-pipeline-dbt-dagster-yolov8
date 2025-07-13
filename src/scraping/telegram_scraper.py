# File Path: src/scraping/telegram_scraper.py
# Date: 10 July 2025
# Developed by: Addisu Taye Dadi
# Purpose: Scrape public Telegram channels using Telethon.
# Key Features:
# - Scrapes messages and images from specified Ethiopian medical channels.
# - Saves raw JSON in structured partitioned directories.
# - Implements logging for error tracking and audit trails.

from telethon.sync import TelegramClient
from datetime import datetime
import os
import json
import logging
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Configure logging
logging.basicConfig(filename='scraping.log', level=logging.INFO)

# Load credentials
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

async def scrape_channel(channel_url):
    async with TelegramClient('session_name', api_id, api_hash) as client:
        try:
            channel = await client.get_entity(channel_url)
            messages = []

            async for message in client.iter_messages(channel):
                messages.append(json.loads(message.to_json()))

            today = datetime.now().strftime('%Y-%m-%d')
            dir_path = f"data/raw/telegram_messages/{today}"
            os.makedirs(dir_path, exist_ok=True)
            file_path = f"{dir_path}/{channel.username}.json"

            with open(file_path, 'w') as f:
                json.dump(messages, f, indent=2)

            logging.info(f"Scraped {len(messages)} messages from {channel_url}")
        except Exception as e:
            logging.error(f"Error scraping {channel_url}: {e}")

if __name__ == "__main__":
    channels = [
        'chemed123',
        'lobelia4cosmetics',
       'tikvahpharma'
       
    ]
    loop = asyncio.get_event_loop()
    for channel in channels:
        loop.run_until_complete(scrape_channel(channel))