# Deployment Guide

## Option A: student-friendly cloud deployment
Recommended layout:
- Database: Supabase PostgreSQL
- Backend: Render Web Service
- Frontend: Render Static Site
- Simulator: run locally on the student's PC during demonstrations, or use a separate worker/job only if the platform plan supports it.

Supabase provides a full PostgreSQL database. Render supports FastAPI web services and React/static sites. Render's free web services can spin down after inactivity and its free Postgres has time/storage limitations, so treat the free tier as coursework/demo infrastructure rather than production. See official documentation linked from the main README.

### Supabase
1. Create a project.
2. Open Database -> Connect and copy a PostgreSQL connection string.
3. Use a connection string compatible with `psycopg2`, for example `postgresql+psycopg2://...`.
4. Do not put the password in Git.
5. Create the database tables by starting the backend once; SQLAlchemy creates the tables for this educational project.
6. For a production deployment, replace automatic table creation with Alembic migrations and enable stricter database roles/RLS policies.

### Render backend
1. Push the repository to GitHub.
2. Create a Render Web Service from the repository.
3. Root directory: `backend`.
4. Build command: `pip install -r requirements.txt`.
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
6. Add environment variables: `DATABASE_URL`, `JWT_SECRET`, `SIMULATOR_API_KEY`, `CORS_ORIGINS`, `OFFLINE_AFTER_SECONDS`.
7. Deploy and open `/health`.

### Render frontend
1. Create a Static Site from the same repository.
2. Root directory: `frontend`.
3. Build command: `npm install && npm run build`.
4. Publish directory: `dist`.
5. Add `VITE_API_URL=https://YOUR-BACKEND.onrender.com`.
6. Update backend `CORS_ORIGINS` to the frontend URL and redeploy backend.

### Cloud demonstration
Register a new account in the public dashboard, create a device, then run the simulator locally with the public backend URL:
```powershell
$env:API_URL="https://YOUR-BACKEND.onrender.com"
$env:SIMULATOR_API_KEY="YOUR_DEVICE_KEY"
py sensor_simulator/simulator.py --device-id PLANT-001 --scenario low-moisture --interval 10
```

## Option B: enterprise AWS-style architecture
`ESP32/Simulator -> AWS IoT Core or API Gateway -> Lambda -> DynamoDB/Timestream -> SNS -> React/S3`

- AWS IoT Core: device identity, MQTT broker, device shadows/rules.
- API Gateway: HTTPS API front door.
- Lambda: validation and automation functions.
- DynamoDB: device/config/event data; Timestream: high-volume time-series telemetry.
- SNS: notifications.
- S3 + CloudFront: static React assets.
- CloudWatch: logs, metrics and alarms.
- Secrets Manager: database/API secrets.
- SQS/EventBridge/Kinesis: buffering/event streaming at larger scale.

### Azure mapping
IoT Hub -> API Management/Azure Functions -> Azure Database for PostgreSQL/Cosmos DB -> Event Grid/Service Bus -> Notification Hubs/Communication Services -> Static Web Apps -> Azure Monitor.

### GCP mapping
Cloud IoT-style architecture can use Pub/Sub as the ingestion/event layer -> Cloud Run/Cloud Functions -> Cloud SQL/Firestore/BigQuery -> Cloud Monitoring/Logging -> Cloud Storage + Cloud CDN for frontend assets.
