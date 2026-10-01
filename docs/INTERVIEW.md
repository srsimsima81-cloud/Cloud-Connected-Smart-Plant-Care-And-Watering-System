# Interview Preparation

### 1. Why is this a cloud project?
Because telemetry is sent to a remotely deployable backend and stored in a managed cloud PostgreSQL database, while the dashboard and API can be independently deployed.

### 2. Why use REST instead of MQTT?
REST is simpler for a student demonstration and works well for periodic telemetry. MQTT is preferable for large fleets and constrained devices because it is broker-based publish/subscribe and supports lightweight messaging.

### 3. Why PostgreSQL instead of SQLite in the cloud?
SQLite is file-based and best for local demos. Managed PostgreSQL supports concurrent clients, remote access, backups/operations and cloud database workflows.

### 4. How is automatic watering prevented from looping?
The backend checks auto-water configuration, tank level, pump state and cooldown. Pump duration is capped and the maintenance loop turns the pump off after the configured duration.

### 5. What happens if the simulator stops?
`last_seen` stops changing. After the configured interval, the backend creates a device-offline alert. When readings resume, the offline alert is resolved and a recovery alert is created.

### 6. How would you scale to 100,000 devices?
Use MQTT/IoT broker ingestion, API gateways, horizontally scalable/stateless consumers, queues/event streams, serverless processing, partitioned/time-series storage, indexes, retention policies and caching.

### 7. What is the difference between authentication and authorization?
Authentication verifies who the caller is; authorization verifies what that caller is allowed to access. This project uses JWT authentication and device ownership checks for authorization.

### 8. What would you improve for production?
Managed identity/certificates, RLS/least privilege, secret manager, rate limiting, migrations, observability, retries with backoff, message queues, device shadows, IaC and CI/CD.
