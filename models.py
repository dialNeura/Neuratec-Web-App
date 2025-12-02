# app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(10))
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True)
    type = Column(String)
    specs = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class SimulationResult(Base):
    __tablename__ = "simulations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
