# File Path: src/dagster_pipeline/pipeline_definition.py
# Date: 10 July 2025
# Developed by: Addisu Taye Dadi
# Purpose: Define ops and jobs in Dagster.
# Key Features:
# - Defines individual tasks as Dagster ops.
# - Creates a job to run the full pipeline.
# - Logs execution status for each step.

from dagster import op, job
import asyncio
import subprocess
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

#
# 📥 Op 1: Scrape Telegram Data
#

@op(description="Scrape messages from Telegram channels using Telethon")
def scrape_telegram_data():
    """
    Scrapes messages from a predefined list of Ethiopian medical Telegram channels.
    Uses asyncio to handle async scraping function.
    """
    from src.scraping.telegram_scraper import scrape_channel
    
    CHANNELS = ['chemed123','lobelia4cosmetics', 'tikvahpharma']
    
    logger.info("Starting Telegram scraping process...")
    
    async def run_scrape():
        for channel in CHANNELS:
            logger.info(f"Scraping data from channel: {channel}")
            await scrape_channel(channel)
    
    asyncio.run(run_scrape())
    
    logger.info("Finished scraping all channels.")

#
# 🗃️ Op 2: Load Raw JSON to PostgreSQL
#

@op(description="Load raw JSON files into PostgreSQL database")
def load_raw_to_postgres():
    """
    Loads raw scraped Telegram data (JSON) into PostgreSQL's raw schema.
    This prepares the data for transformation via dbt.
    """
    logger.info("Loading raw data into PostgreSQL...")
    
    # Replace with actual implementation or call external script
    try:
        subprocess.run(["python", "src/scraping/load_data.py"], check=True)
        logger.info("Raw data successfully loaded into PostgreSQL.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to load raw data: {e}")
        raise

#
# 🏗️ Op 3: Run dbt Transformations
#

@op(description="Run dbt models to transform raw data into structured tables")
def run_dbt_transformations():
    """
    Executes dbt models to clean, restructure, and model the data into a dimensional star schema.
    """
    logger.info("Running dbt transformations...")
    
    try:
        result = subprocess.run(
            ["cd", "src/dbt_project", "&&", "dbt", "run"],
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("dbt transformation completed successfully.")
        logger.debug(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"dbt transformation failed: {e.stderr}")
        raise

#
# 🖼️ Op 4: Enrich Images Using YOLOv8
#

@op(description="Run YOLOv8 object detection on downloaded images")
def run_yolo_enrichment():
    """
    Runs YOLOv8 inference on downloaded Telegram images to extract visual insights.
    Results are inserted into the warehouse for analysis.
    """
    logger.info("Running YOLO image detection...")
    
    try:
        result = subprocess.run(
            ["python", "src/yolo/image_analyzer.py"],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("YOLO enrichment completed successfully.")
        logger.debug(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"YOLO enrichment failed: {e.stderr}")
        raise

#
# ⚙️ Job Definition: Full Pipeline
#

@job(description="Full end-to-end pipeline: scrape → load → transform → enrich")
def full_pipeline():
    """
    Defines the full DAG of operations to be orchestrated by Dagster.
    Execution order:
        1. Scrape Telegram messages
        2. Load into PostgreSQL
        3. Transform using dbt
        4. Enrich with YOLOv8
    """
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()
