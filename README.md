# File Path: README.md
# Date: 10 July 2025
# Developed by: Addisu Taye Dadi
# Purpose: Provide an overview of the project structure and usage instructions.
# Key Features:
# - Includes project purpose, architecture, setup steps, and contribution guidelines.

# Telegram Data Pipeline

## Overview

This project builds an end-to-end data pipeline that scrapes public Telegram channels, transforms data using dbt, enriches images with YOLOv8, and exposes insights through a FastAPI endpoint. It uses Dagster for orchestration and PostgreSQL as a warehouse.

## Architecture

- **Data Lake**: Raw JSON in `data/raw/`
- **Warehouse**: PostgreSQL
- **Transformations**: dbt models
- **Enrichment**: YOLOv8 for image object detection
- **API**: FastAPI
- **Orchestration**: Dagster

## Setup Instructions

1. Clone repo
2. Set up `.env` with your Telegram API credentials
3. Run `docker-compose up -d`
4. Install requirements: `pip install -r requirements.txt`
5. Start scraping: `python src/scraping/telegram_scraper.py`
6. Run dbt: `cd src/dbt_project && dbt run`
7. Launch FastAPI: `uvicorn src/api.main:app --reload`
8. Start Dagster: `dagster dev`

## License

MIT