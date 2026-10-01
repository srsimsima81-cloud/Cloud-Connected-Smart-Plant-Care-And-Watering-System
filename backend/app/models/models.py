from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from ..db import Base

def utcnow(): return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    devices = relationship('Device', back_populates='user', cascade='all, delete-orphan')

class Device(Base):
    __tablename__ = 'devices'
    device_id = Column(String(80), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, index=True)
    plant_name = Column(String(120), nullable=False)
    plant_type = Column(String(80), nullable=False)
    location = Column(String(160), nullable=False)
    moisture_threshold = Column(Float, nullable=False, default=30)
    temperature_threshold = Column(Float, nullable=False, default=35)
    humidity_minimum = Column(Float, nullable=False, default=30)
    tank_minimum = Column(Float, nullable=False, default=15)
    watering_duration = Column(Integer, nullable=False, default=5)
    cooldown_seconds = Column(Integer, nullable=False, default=30)
    auto_water = Column(Boolean, nullable=False, default=True)
    pump_on = Column(Boolean, nullable=False, default=False)
    pump_started_at = Column(DateTime(timezone=True), nullable=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    user = relationship('User', back_populates='devices')
    readings = relationship('SensorReading', back_populates='device', cascade='all, delete-orphan')
    watering_events = relationship('WateringEvent', back_populates='device', cascade='all, delete-orphan')
    alerts = relationship('Alert', back_populates='device', cascade='all, delete-orphan')

class SensorReading(Base):
    __tablename__ = 'sensor_readings'
    reading_id = Column(Integer, primary_key=True)
    device_id = Column(String(80), ForeignKey('devices.device_id'), nullable=False, index=True)
    soil_moisture = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    light_level = Column(Float, nullable=True)
    water_tank_level = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=utcnow, nullable=False, index=True)
    reading_key = Column(String(120), nullable=False)
    device = relationship('Device', back_populates='readings')
    __table_args__ = (UniqueConstraint('device_id', 'reading_key', name='uq_device_reading_key'), Index('ix_reading_device_time', 'device_id', 'timestamp'))

class WateringEvent(Base):
    __tablename__ = 'watering_events'
    event_id = Column(Integer, primary_key=True)
    device_id = Column(String(80), ForeignKey('devices.device_id'), nullable=False, index=True)
    trigger_type = Column(String(30), nullable=False)
    moisture_before = Column(Float, nullable=True)
    moisture_after = Column(Float, nullable=True)
    duration = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    status = Column(String(30), nullable=False, default='started')
    device = relationship('Device', back_populates='watering_events')

class Alert(Base):
    __tablename__ = 'alerts'
    alert_id = Column(Integer, primary_key=True)
    device_id = Column(String(80), ForeignKey('devices.device_id'), nullable=False, index=True)
    alert_type = Column(String(50), nullable=False)
    level = Column(String(20), nullable=False)
    message = Column(String(500), nullable=False)
    status = Column(String(20), nullable=False, default='open')
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    device = relationship('Device', back_populates='alerts')
