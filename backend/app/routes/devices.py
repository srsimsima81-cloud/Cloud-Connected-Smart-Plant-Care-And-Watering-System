from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User, Device, SensorReading, WateringEvent, Alert
from ..schemas import DeviceCreate, ThresholdUpdate, WaterRequest, SensorData
from ..utils.auth import current_user
from ..utils.serialization import device_dict, reading_dict, event_dict, alert_dict
from ..services.automation import start_pump
from ..services.realtime import manager
router=APIRouter(prefix='/api/devices',tags=['Devices'])

def owned(db, user, device_id):
    d=db.query(Device).filter(Device.device_id==device_id,Device.user_id==user.user_id).first()
    if not d: raise HTTPException(404,'Device not found')
    return d
@router.get('')
def list_devices(db:Session=Depends(get_db), user:User=Depends(current_user)): return [device_dict(x) for x in db.query(Device).filter(Device.user_id==user.user_id).all()]
@router.post('',status_code=201)
def create_device(data:DeviceCreate,db:Session=Depends(get_db),user:User=Depends(current_user)):
    if db.get(Device,data.device_id): raise HTTPException(409,'Device ID already exists')
    vals=data.model_dump();
    if vals.get('moisture_threshold') is None:
        from automation.plant_profiles import threshold_for
        vals['moisture_threshold']=threshold_for(vals['plant_type'])
    d=Device(**vals,user_id=user.user_id); db.add(d); db.commit(); db.refresh(d); return device_dict(d)
@router.get('/{device_id}')
def get_device(device_id:str,db:Session=Depends(get_db),user:User=Depends(current_user)): return device_dict(owned(db,user,device_id))
@router.get('/{device_id}/latest')
def latest(device_id:str,db:Session=Depends(get_db),user:User=Depends(current_user)):
    d=owned(db,user,device_id); r=db.query(SensorReading).filter(SensorReading.device_id==d.device_id).order_by(SensorReading.timestamp.desc()).first(); return reading_dict(r) if r else None
@router.get('/{device_id}/history')
def history(device_id:str,limit:int=200,db:Session=Depends(get_db),user:User=Depends(current_user)):
    d=owned(db,user,device_id); return [reading_dict(x) for x in db.query(SensorReading).filter(SensorReading.device_id==d.device_id).order_by(SensorReading.timestamp.desc()).limit(min(limit,1000)).all()][::-1]
@router.put('/{device_id}/threshold')
def threshold(device_id:str,data:ThresholdUpdate,db:Session=Depends(get_db),user:User=Depends(current_user)):
    d=owned(db,user,device_id); vals=data.model_dump(exclude_none=True)
    for k,v in vals.items(): setattr(d,k,v)
    db.commit(); return device_dict(d)
@router.post('/{device_id}/water')
async def water(device_id:str,data:WaterRequest,db:Session=Depends(get_db),user:User=Depends(current_user)):
    d=owned(db,user,device_id)
    if d.pump_on: raise HTTPException(409,'Pump is already running')
    last=db.query(SensorReading).filter(SensorReading.device_id==d.device_id).order_by(SensorReading.timestamp.desc()).first()
    if data.duration: d.watering_duration=data.duration
    start_pump(db,d,'manual',last.soil_moisture if last else None);
    db.commit(); await manager.broadcast({'type':'device_update','device_id':d.device_id}); return device_dict(d)

@router.get('/{device_id}/control-state')
def control_state(device_id:str, db:Session=Depends(get_db), x_simulator_key:str|None=Header(default=None)):
    from ..config import settings
    if x_simulator_key != settings.simulator_api_key: raise HTTPException(401,'Invalid simulator key')
    d=db.get(Device,device_id)
    if not d: raise HTTPException(404,'Device not found')
    return {'device_id':d.device_id,'pump_on':d.pump_on,'watering_duration':d.watering_duration,'auto_water':d.auto_water,'moisture_threshold':d.moisture_threshold}

@router.get('/{device_id}/watering-history')
def watering_history(device_id:str,db:Session=Depends(get_db),user:User=Depends(current_user)):
    d=owned(db,user,device_id); return [event_dict(x) for x in db.query(WateringEvent).filter(WateringEvent.device_id==d.device_id).order_by(WateringEvent.timestamp.desc()).limit(100).all()]
