from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
class TokenResponse(BaseModel): token: str
class DeviceCreate(BaseModel):
    device_id: str = Field(min_length=2, max_length=80)
    plant_name: str = Field(min_length=1, max_length=120)
    plant_type: str = Field(min_length=1, max_length=80)
    location: str = Field(min_length=1, max_length=160)
    moisture_threshold: Optional[float] = Field(default=None, ge=0, le=100)
    temperature_threshold: float = Field(default=35, ge=0, le=80)
    humidity_minimum: float = Field(default=30, ge=0, le=100)
    tank_minimum: float = Field(default=15, ge=0, le=100)
    watering_duration: int = Field(default=5, ge=1, le=60)
    cooldown_seconds: int = Field(default=30, ge=5, le=86400)
    auto_water: bool = True
class ThresholdUpdate(BaseModel):
    moisture_threshold: float = Field(ge=0, le=100)
    temperature_threshold: Optional[float] = Field(default=None, ge=0, le=80)
    humidity_minimum: Optional[float] = Field(default=None, ge=0, le=100)
    tank_minimum: Optional[float] = Field(default=None, ge=0, le=100)
    auto_water: Optional[bool] = None
class SensorData(BaseModel):
    device_id: str
    soil_moisture: float = Field(ge=0, le=100)
    temperature: float = Field(ge=-20, le=80)
    humidity: float = Field(ge=0, le=100)
    light_level: Optional[float] = Field(default=None, ge=0, le=100)
    water_tank_level: Optional[float] = Field(default=None, ge=0, le=100)
    timestamp: Optional[datetime] = None
    reading_key: Optional[str] = None
class WaterRequest(BaseModel): duration: Optional[int] = Field(default=None, ge=1, le=60)
class AckRequest(BaseModel): status: str = Field(pattern='^(acknowledged)$')
