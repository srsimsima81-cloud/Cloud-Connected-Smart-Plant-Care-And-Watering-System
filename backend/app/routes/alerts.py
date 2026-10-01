from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User, Device, Alert
from ..schemas import AckRequest
from ..utils.auth import current_user
from ..utils.serialization import alert_dict
router=APIRouter(prefix='/api/alerts',tags=['Alerts'])
@router.get('')
def alerts(db:Session=Depends(get_db),user:User=Depends(current_user)):
    ids=[x.device_id for x in db.query(Device).filter(Device.user_id==user.user_id).all()]
    return [alert_dict(a) for a in db.query(Alert).filter(Alert.device_id.in_(ids)).order_by(Alert.created_at.desc()).limit(100).all()]
@router.put('/{alert_id}/acknowledge')
def acknowledge(alert_id:int,data:AckRequest,db:Session=Depends(get_db),user:User=Depends(current_user)):
    a=db.get(Alert,alert_id); d=db.get(Device,a.device_id) if a else None
    if not a or not d or d.user_id!=user.user_id: raise HTTPException(404,'Alert not found')
    a.status='acknowledged'; from datetime import datetime,timezone; a.acknowledged_at=datetime.now(timezone.utc); db.commit(); return alert_dict(a)
