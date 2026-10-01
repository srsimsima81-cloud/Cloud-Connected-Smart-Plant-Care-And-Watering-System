from datetime import datetime, timezone
from ..config import settings
from ..models import Device, Alert

def check_offline(db):
    now=datetime.now(timezone.utc)
    for d in db.query(Device).all():
        ls=d.last_seen.replace(tzinfo=timezone.utc) if d.last_seen and d.last_seen.tzinfo is None else d.last_seen
        if ls and (now-ls).total_seconds()>settings.offline_after_seconds:
            exists=db.query(Alert).filter(Alert.device_id==d.device_id,Alert.alert_type=='DEVICE_OFFLINE',Alert.status=='open').first()
            if not exists: db.add(Alert(device_id=d.device_id,alert_type='DEVICE_OFFLINE',level='CRITICAL',message=f'No sensor data received from {d.device_id} during the expected interval.'))
        elif ls:
            open_offline=db.query(Alert).filter(Alert.device_id==d.device_id,Alert.alert_type=='DEVICE_OFFLINE',Alert.status=='open').all()
            if open_offline:
                for a in open_offline: a.status='resolved'
                db.add(Alert(device_id=d.device_id,alert_type='DEVICE_RECOVERED',level='INFO',message=f'{d.device_id} reconnected and resumed sensor reporting.'))
    db.commit()
