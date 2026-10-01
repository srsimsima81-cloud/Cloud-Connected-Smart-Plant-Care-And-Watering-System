from datetime import datetime, timezone
import hashlib
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Device, SensorReading
from ..schemas import SensorData
from ..config import settings
from ..services.automation import evaluate_reading
from ..services.realtime import manager
router=APIRouter(prefix='/api/sensors',tags=['Sensors'])
@router.post('/data')
async def ingest(data:SensorData, db:Session=Depends(get_db), x_simulator_key:str|None=Header(default=None)):
    # Simulator authentication is intentionally separate from user JWT auth.
    if x_simulator_key != settings.simulator_api_key: raise HTTPException(401,'Invalid simulator key')
    d=db.get(Device,data.device_id)
    if not d: raise HTTPException(404,'Device not found')
    ts=data.timestamp or datetime.now(timezone.utc); key=data.reading_key or hashlib.sha256(f'{data.device_id}|{ts.isoformat()}|{data.soil_moisture}|{data.temperature}'.encode()).hexdigest()
    if db.query(SensorReading).filter(SensorReading.device_id==d.device_id,SensorReading.reading_key==key).first(): return {'status':'duplicate','device_id':d.device_id}
    r=SensorReading(device_id=d.device_id,soil_moisture=data.soil_moisture,temperature=data.temperature,humidity=data.humidity,light_level=data.light_level,water_tank_level=data.water_tank_level,timestamp=ts,reading_key=key)
    db.add(r); d.last_seen=datetime.now(timezone.utc); db.flush(); evaluate_reading(db,d,r); db.commit()
    await manager.broadcast({'type':'sensor_update','device_id':d.device_id,'reading':{'soil_moisture':r.soil_moisture,'temperature':r.temperature,'humidity':r.humidity,'light_level':r.light_level,'water_tank_level':r.water_tank_level,'timestamp':r.timestamp.isoformat()},'pump_on':d.pump_on})
    return {'status':'accepted','reading_id':r.reading_id,'pump_on':d.pump_on}
