# File Path: src/api/crud.py
# Date: July 10, 2025
# Developed by: Addisu Taye Dadi
# Purpose: Handle actual querying of dbt models
# Key Features:
# - Uses SQLAlchemy to query dbt-transformed data
# - Modularizes query logic for reuse

from sqlalchemy.engine import Engine
from typing import List

def get_top_products(engine: Engine, limit: int = 10) -> List[dict]:
    result = engine.execute(f"""
        SELECT message_text, COUNT(*) AS count
        FROM fct_messages
        WHERE message_text ILIKE '%paracetamol%' OR message_text ILIKE '%ibuprofen%'
        GROUP BY message_text
        ORDER BY count DESC
        LIMIT {limit}
    """).fetchall()
    return [{"product": r[0], "count": r[1]} for r in result]

def get_channel_activity(engine: Engine, channel_name: str) -> List[dict]:
    result = engine.execute(f"""
        SELECT d.year, d.month_name, COUNT(*) AS message_count
        FROM fct_messages m
        JOIN dim_channels c ON m.channel_id = c.channel_id
        JOIN dim_dates d ON DATE(m.message_date) = d.date
        WHERE c.channel_name = '{channel_name}'
        GROUP BY d.year, d.month_name
        ORDER BY d.date
    """).fetchall()
    return [{"year": r[0], "month": r[1], "message_count": r[2]} for r in result]