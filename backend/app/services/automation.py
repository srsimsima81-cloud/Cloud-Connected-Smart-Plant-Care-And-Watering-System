from datetime import datetime, timezone
from sqlalchemy.orm import Session
from ..models import Device, SensorReading, WateringEvent, Alert

def now(): return datetime.now(timezone.utc)
def create_alert(db, device, alert_type, level, message):
    existing=db.query(Alert).filter(Alert.device_id==device.device_id,Alert.alert_type==alert_type,Alert.status=='open').first()
    if not existing: db.add(Alert(device_id=device.device_id,alert_type=alert_type,level=level,message=message))
def evaluate_reading(db:Session,device:Device,reading:SensorReading):
    if reading.soil_moisture < device.moisture_threshold:
        create_alert(db,device,'LOW_SOIL_MOISTURE','WARNING',f'{device.plant_name} moisture dropped below {device.moisture_threshold:.0f}%.')
        if device.auto_water and (reading.water_tank_level is None or reading.water_tank_level >= device.tank_minimum):
            last=db.query(WateringEvent).filter(WateringEvent.device_id==device.device_id).order_by(WateringEvent.timestamp.desc()).first()
            if last and last.timestamp:
                lt=last.timestamp.replace(tzinfo=timezone.utc) if last.timestamp.tzinfo is None else last.timestamp
                elapsed=(now()-lt).total_seconds()
            else: elapsed=10**9
            if not device.pump_on and elapsed >= device.cooldown_seconds: start_pump(db,device,'automatic',reading.soil_moisture)
    else:
        for a in db.query(Alert).filter(Alert.device_id==device.device_id,Alert.alert_type=='LOW_SOIL_MOISTURE',Alert.status=='open'): a.status='resolved'
    if reading.temperature > device.temperature_threshold: create_alert(db,device,'HIGH_TEMPERATURE','WARNING',f'{device.plant_name} temperature exceeded {device.temperature_threshold:.0f}°C.')
    if reading.humidity < device.humidity_minimum: create_alert(db,device,'LOW_HUMIDITY','INFO',f'{device.plant_name} humidity fell below {device.humidity_minimum:.0f}%.')
    if reading.water_tank_level is not None and reading.water_tank_level < device.tank_minimum: create_alert(db,device,'LOW_WATER_TANK','CRITICAL',f'{device.plant_name} water tank is below {device.tank_minimum:.0f}%.')
def start_pump(db,device,trigger,moisture):
    device.pump_on=True; device.pump_started_at=now(); db.add(WateringEvent(device_id=device.device_id,trigger_type=trigger,moisture_before=moisture,duration=device.watering_duration,status='started'))
def stop_expired_pumps(db:Session):
    for d in db.query(Device).filter(Device.pump_on==True).all():
        if not d.pump_started_at: continue
        pt=d.pump_started_at.replace(tzinfo=timezone.utc) if d.pump_started_at.tzinfo is None else d.pump_started_at
        if (now()-pt).total_seconds() >= d.watering_duration:
            event=db.query(WateringEvent).filter(WateringEvent.device_id==d.device_id,WateringEvent.status=='started').order_by(WateringEvent.timestamp.desc()).first()
            d.pump_on=False; d.pump_started_at=None
            if event: event.status='completed'
    db.commit()
