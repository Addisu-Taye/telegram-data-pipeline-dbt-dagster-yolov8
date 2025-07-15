# File Path: src/api/models.py
# Date: July 10, 2025
# Developed by: Addisu Taye Dadi
# Purpose: ORM-style definitions for querying fact and dimension tables
# Key Features:
# - Reflects schema from dbt models
# - Used for raw SQL or ORM-based queries

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FactMessage(Base):
    __tablename__ = 'fct_messages'
    
    message_id = Column(Integer, primary_key=True)
    message_text = Column(String)
    message_date = Column(DateTime)
    channel_id = Column(Integer, ForeignKey('dim_channels.channel_id'))
    has_image = Column(Integer)

class DimChannel(Base):
    __tablename__ = 'dim_channels'
    
    channel_id = Column(Integer, primary_key=True)
    channel_name = Column(String)

class DimDate(Base):
    __tablename__ = 'dim_dates'
    
    date = Column(String, primary_key=True)
    year = Column(Integer)
    month_name = Column(String)