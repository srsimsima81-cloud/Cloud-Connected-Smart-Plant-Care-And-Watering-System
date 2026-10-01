import os
os.environ['DATABASE_URL']='sqlite:///./test_plantcare.db'
os.environ['JWT_SECRET']='test-secret'
os.environ['SIMULATOR_API_KEY']='test-key'
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db import Base,engine
Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
client=TestClient(app)

def auth():
    r=client.post('/api/auth/register',json={'name':'Ava Morgan','email':'ava@example.com','password':'strongpass123'}); return {'Authorization':'Bearer '+r.json()['token']}

def test_registration_and_device():
    h=auth(); r=client.post('/api/devices',headers=h,json={'device_id':'PLANT-TEST','plant_name':'Tomato','plant_type':'TOMATO','location':'Balcony'}); assert r.status_code==201

def test_invalid_sensor_rejected():
    r=client.post('/api/sensors/data',headers={'X-Simulator-Key':'test-key'},json={'device_id':'PLANT-TEST','soil_moisture':150,'temperature':30,'humidity':50}); assert r.status_code==422

def test_sensor_ingestion_and_automation():
    r=client.post('/api/sensors/data',headers={'X-Simulator-Key':'test-key'},json={'device_id':'PLANT-TEST','soil_moisture':20,'temperature':28,'humidity':60,'light_level':50,'water_tank_level':90,'reading_key':'unique-1'}); assert r.status_code==200; assert r.json()['pump_on'] is True
