import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from .db import Base,engine,SessionLocal
from .routes import auth,devices,sensors,alerts,analytics
from .services.automation import stop_expired_pumps
from .services.offline import check_offline
from .services.realtime import manager
from .config import settings

Base.metadata.create_all(bind=engine)
app=FastAPI(title='Cloud Smart Plant Care API',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.cors_origins.split(',')],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(auth.router); app.include_router(devices.router); app.include_router(sensors.router); app.include_router(alerts.router); app.include_router(analytics.router)
@app.get('/health')
def health(): return {'status':'ok','service':'cloud-smart-plant-care'}
@app.websocket('/ws')
async def websocket(ws:WebSocket):
    await manager.connect(ws)
    try:
        while True: await ws.receive_text()
    except Exception: manager.disconnect(ws)
async def maintenance():
    while True:
        db=SessionLocal()
        try: stop_expired_pumps(db); check_offline(db)
        finally: db.close()
        await asyncio.sleep(5)
@app.on_event('startup')
async def startup(): app.state.maintenance=asyncio.create_task(maintenance())
@app.on_event('shutdown')
async def shutdown():
    task=getattr(app.state,'maintenance',None)
    if task: task.cancel()
