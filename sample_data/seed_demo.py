"""Optional demo seed. Normal application startup never calls this file."""
import os, sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..'))
os.environ.setdefault('DATABASE_URL','sqlite:///./plantcare.db')
from backend.app.db import SessionLocal
from backend.app.models import User,Device
from backend.app.utils.auth import hash_password

db=SessionLocal()
email='demo@example.com'
u=db.query(User).filter(User.email==email).first()
if not u:
    u=User(name='Demo User',email=email,password_hash=hash_password('DemoPass123!'));db.add(u);db.commit();db.refresh(u)
if not db.get(Device,'PLANT-001'):
    db.add(Device(device_id='PLANT-001',user_id=u.user_id,plant_name='Tomato Plant',plant_type='TOMATO',location='Demo Greenhouse',moisture_threshold=30,auto_water=True))
    db.commit()
print('Demo ready: demo@example.com / DemoPass123! / PLANT-001')
db.close()
