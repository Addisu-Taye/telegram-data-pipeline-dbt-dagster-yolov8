# File Path: src/scraping/image_downloader.py
# Date: 10 July 2025
# Developed by: Addisu Taye Dadi
# Purpose: Download images from Telegram messages.
# Key Features:
# - Extracts media URLs from scraped messages.
# - Downloads and stores images locally for YOLO processing.

from telethon.sync import TelegramClient
from telethon.tl.types import Photo
import os
import logging
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='image_download.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load Telegram API credentials
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

async def download_images(channel_username):
    """
    Asynchronously downloads all images from a given Telegram channel.

    Parameters:
        channel_username (str): The username or URL of the Telegram channel.

    Output:
        Saves images to data/images/channel_username/
    """
    async with TelegramClient('session_name', api_id, api_hash) as client:
        try:
            # Get the channel entity
            channel = await client.get_entity(channel_username)
            logging.info(f"Connected to channel: {channel_username}")

            # Create a directory for storing images
            media_dir = f"data/images/{channel.username}/"
            os.makedirs(media_dir, exist_ok=True)
            logging.info(f"Created image directory: {media_dir}")

            # Iterate over all messages in the channel
            async for message in client.iter_messages(channel):
                if message.photo:
                    try:
                        # Generate a unique file name based on message ID
                        file_path = os.path.join(media_dir, f"{message.id}.jpg")
                        
                        # Download the photo
                        await message.download_media(file=file_path)
                        logging.info(f"Downloaded image: {file_path}")
                        print(f"Downloaded: {file_path}")
                    except Exception as e:
                        logging.error(f"Failed to download image from message {message.id}: {e}")

        except Exception as e:
            logging.error(f"Error connecting to channel {channel_username}: {e}")

if __name__ == "__main__":
    # List of channels to scrape images from
    channels = [
        #'chemed123',
       # 'lobelia4cosmetics',
        'tikvahpharma'
    ]

    # Set up event loop and run the downloader
    loop = asyncio.get_event_loop()
    for channel in channels:
        print(f"Downloading images from channel: {channel}")
        loop.run_until_complete(download_images(channel))