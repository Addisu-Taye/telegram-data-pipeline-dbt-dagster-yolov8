# File Path: src/api/main.py
# Date: 10 July 2025
# Developed by: Addisu Taye Dadi
# Purpose: Main FastAPI application to expose analytical endpoints.
# Key Features:
# - Exposes endpoints to query transformed data from dbt models.
# - Uses Pydantic schemas for validation.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

@app.get("/api/reports/top-products")
def top_products(limit: int = 10):
    result = engine.execute(f"""
        SELECT product_name, COUNT(*) AS count
        FROM fct_messages
        WHERE product_name IS NOT NULL
        GROUP BY product_name
        ORDER BY count DESC
        LIMIT {limit}
    """).fetchall()
    return [{"product": r[0], "count": r[1]} for r in result]