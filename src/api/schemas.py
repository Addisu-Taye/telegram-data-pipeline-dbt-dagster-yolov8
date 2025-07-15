# File Path: src/api/schemas.py
# Date: July 10, 2025
# Developed by: Addisu Taye Dadi
# Purpose: Define Pydantic models for API validation
# Key Features:
# - Ensures consistent input/output structures
# - Helps prevent malformed requests

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
    date: Optional[datetime]
    channel: str