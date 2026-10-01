# Cloud-Connected Smart Plant Care & Watering System

A hardware-free IoT/cloud computing project that simulates plant sensors, sends telemetry to a FastAPI cloud backend, stores readings in PostgreSQL/Supabase or local SQLite, evaluates watering rules, controls a virtual pump, raises alerts, and visualizes live/historical data in React.

## Core stack
- Python 3.11/3.12 + FastAPI + SQLAlchemy
- PostgreSQL (recommended cloud: Supabase); SQLite local fallback
- React + Vite + Recharts
- REST + WebSocket
- JWT user authentication + simulator API key
- Pytest

## Architecture
```text
Python Sensor Simulator / ESP32
          | HTTPS REST
          v
     FastAPI API Layer
       /         \
      v           v
 PostgreSQL     Automation Engine
(Supabase)          |
      ^             v
      |        Virtual Pump
      +---- WebSocket ---> React Dashboard
                       |
                 Alerts + Analytics
```

## Clean startup
The app creates database tables but does **not** insert sample devices, readings, alerts, watering events, or user profiles. Create your own account and device from the UI. Demo data is isolated under `sample_data/`.

## Local run - SQLite
### 1. Backend
```powershell
cd backend
py -m venv .venv
.venv\Scripts\activate
copy .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Open http://127.0.0.1:8000/docs

### 2. Frontend
```powershell
cd frontend
copy .env.example .env
npm install
npm run dev
```
Open the Vite URL shown in the terminal (normally http://localhost:5173).

### 3. Create a device
Register in the UI, then create e.g.:
- Device ID: `PLANT-001`
- Plant name: `Tomato Plant`
- Plant type: `TOMATO`
- Location: `Balcony`
- Moisture threshold: `30`
- Auto watering: enabled

### 4. Run simulator
```powershell
cd sensor_simulator
py simulator.py --device-id PLANT-001 --scenario normal --interval 5
```
Controlled scenarios:
```powershell
py simulator.py --device-id PLANT-001 --scenario low-moisture --interval 5
py simulator.py --device-id PLANT-001 --scenario high-temperature --interval 5
py simulator.py --device-id PLANT-001 --scenario low-humidity --interval 5
py simulator.py --device-id PLANT-001 --scenario low-tank --interval 5
```
Use `Ctrl+C` to stop. A disconnected-device demo is simply done by stopping the simulator and waiting longer than `OFFLINE_AFTER_SECONDS`; restart it to demonstrate recovery.

## Docker local cloud-like run
```powershell
docker compose up --build
```
This starts PostgreSQL and FastAPI. Run the React frontend separately with `npm run dev`.

## Optional demo seed
Only run this when you intentionally want demo data:
```powershell
py sample_data/seed_demo.py
```
It creates `demo@example.com`, password `DemoPass123!`, and `PLANT-001`. Change/remove demo credentials before any public deployment.

## Cloud deployment
Recommended student architecture: React static site + FastAPI web service + Supabase PostgreSQL. Supabase provides managed Postgres; Render can host FastAPI and static React sites. Render's free services have sleep/usage limitations, so this is suitable for coursework/demo use rather than production. See `docs/DEPLOYMENT.md`.

## Security
Never commit `.env`, passwords, JWT secrets, or cloud database credentials. Use platform environment variables. The simulator uses a separate ingestion key, while dashboard users use JWT authentication. Production should add per-device credentials, HTTPS-only traffic, rate limiting, secret rotation, stronger device identity, and managed secret storage.

## Optional ESP32
The same JSON schema and `/api/sensors/data` endpoint can accept ESP32 readings. See `docs/ESP32.md` and `sensor_simulator/esp32/plantcare_esp32.ino`.

## Testing
```powershell
$env:PYTHONPATH="."
pytest -q
```

## GitHub proof-of-work
Commit architecture, source, tests, API docs, deployment notes, controlled simulator scenarios, screenshots, and a short report. Never commit secrets or real personal credentials.
