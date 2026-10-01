import argparse, json, logging, math, random, time
from datetime import datetime, timezone
import urllib.request, urllib.error
from config import API_URL,DEVICE_ID,SIMULATOR_API_KEY,INTERVAL,SCENARIO
logging.basicConfig(level=logging.INFO,format='%(asctime)s | %(levelname)s | %(message)s'); log=logging.getLogger('simulator')

def post(payload):
    delay=1
    for attempt in range(1,4):
        req=urllib.request.Request(API_URL+'/api/sensors/data',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json','X-Simulator-Key':SIMULATOR_API_KEY},method='POST')
        try:
            with urllib.request.urlopen(req,timeout=5) as r: return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body=e.read().decode(errors='ignore')
            log.error('API rejected reading (attempt %s/3): HTTP %s %s',attempt,e.code,body)
            if 400 <= e.code < 500: return None
        except Exception as e:
            log.error('API send failed (attempt %s/3): %s',attempt,e)
        if attempt<3: time.sleep(delay); delay*=2
    log.error('Reading dropped after retries; next cycle will continue.')
    return None

def control_state():
    try:
        req=urllib.request.Request(API_URL+f'/api/devices/{DEVICE_ID}/latest')
        with urllib.request.urlopen(req,timeout=3) as r: return json.loads(r.read()) or {}
    except Exception: return {}

def generate(device_id, step, scenario, pump=False):
    # Deterministic presets make screenshot/testing scenarios reproducible.

    if scenario == 'low-moisture':
        # First few readings create the problem.
        if step < 4:
            soil = 28
        # Then simulate the effect of watering/recovery.
        elif step < 8:
            soil = 48
        else:
            soil = 50 + 3 * math.sin(step / 4)

        temp = 28 + 0.2 * math.sin(step)
        hum = 55

    elif scenario == 'high-temperature':
        soil = max(25, 55 - step * 0.5)
        temp = 37
        hum = 45

    elif scenario == 'low-humidity':
        soil = max(30, 55 - step * 0.3)
        temp = 31
        hum = 20

    elif scenario == 'low-tank':
        soil = max(25, 55 - step * 0.2)
        temp = 29
        hum = 55

    else:
        # Normal scenario: moisture remains in a healthy range.
        soil = 50 + 5 * math.sin(step / 4)
        temp = 28 + 2 * math.sin(step / 4)
        hum = 60 + 5 * math.sin(step / 5)

    light = max(
        0,
        min(100, 50 + 45 * math.sin((step % 24) / 24 * 2 * math.pi))
    )

    tank = 8 if scenario == 'low-tank' else max(0, 85 - step * 0.05)

    return {
        'device_id': device_id,
        'soil_moisture': round(soil, 2),
        'temperature': round(temp, 2),
        'humidity': round(hum, 2),
        'light_level': round(light, 2),
        'water_tank_level': round(tank, 2),
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'reading_key': f'{device_id}-{scenario}-{datetime.now(timezone.utc).timestamp()}'
    }

def main():
    p=argparse.ArgumentParser(); p.add_argument('--device-id',default=DEVICE_ID); p.add_argument('--scenario',choices=['normal','low-moisture','high-temperature','low-humidity','low-tank'],default=SCENARIO); p.add_argument('--interval',type=float,default=INTERVAL); p.add_argument('--once',action='store_true'); args=p.parse_args()
    if not args.device_id: raise SystemExit('Set --device-id to an existing device ID.')
    step=0; log.info('Simulator started: device=%s scenario=%s',args.device_id,args.scenario)
    while True:
        pump=False
        try:
            req=urllib.request.Request(API_URL+f'/api/devices/{args.device_id}/control-state')
            with urllib.request.urlopen(req,timeout=3) as r: pump=json.loads(r.read()).get('pump_on',False)
        except Exception: pass
        payload=generate(args.device_id,step,args.scenario,pump); result=post(payload); log.info('soil=%s temp=%s humidity=%s tank=%s result=%s',payload['soil_moisture'],payload['temperature'],payload['humidity'],payload['water_tank_level'],result)
        step+=1
        if args.once: break
        time.sleep(args.interval)
if __name__=='__main__': main()
