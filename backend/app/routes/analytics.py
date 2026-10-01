from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db import get_db
from ..models import User,Device,SensorReading,WateringEvent
from ..utils.auth import current_user
router=APIRouter(prefix='/api/analytics',tags=['Analytics'])
@router.get('/{device_id}')
def analytics(device_id:str,db:Session=Depends(get_db),user:User=Depends(current_user)):
    d=db.query(Device).filter(Device.device_id==device_id,Device.user_id==user.user_id).first()
    if not d: return {'error':'Device not found'}
    q=db.query(SensorReading).filter(SensorReading.device_id==device_id); count=q.count()
    def avg(col): return round(float(db.query(func.avg(col)).filter(SensorReading.device_id==device_id).scalar() or 0),2)
    def mn(col): return float(db.query(func.min(col)).filter(SensorReading.device_id==device_id).scalar() or 0)
    def mx(col): return float(db.query(func.max(col)).filter(SensorReading.device_id==device_id).scalar() or 0)
    return {'reading_count':count,'average_soil_moisture':avg(SensorReading.soil_moisture),'min_moisture':mn(SensorReading.soil_moisture),'max_moisture':mx(SensorReading.soil_moisture),'average_temperature':avg(SensorReading.temperature),'average_humidity':avg(SensorReading.humidity),'watering_events':db.query(WateringEvent).filter(WateringEvent.device_id==device_id).count()}
