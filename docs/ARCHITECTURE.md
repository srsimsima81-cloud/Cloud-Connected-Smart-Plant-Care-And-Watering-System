# Architecture and Cloud Concepts

## Simple explanation
A virtual sensor behaves like an ESP32. It measures simulated soil moisture, temperature, humidity, light and tank level. It sends those readings over HTTPS to the backend. The backend validates and stores the reading, evaluates plant rules, and can turn on a virtual pump. The React dashboard retrieves history and receives near-real-time updates through WebSocket.

## Technical flow
`Simulator/ESP32 -> HTTPS REST -> FastAPI -> PostgreSQL -> Automation -> Virtual Pump -> WebSocket/REST -> React`

## Cloud concepts mapped to this project
| Concept | Project location |
|---|---|
| Cloud computing | Backend and database can run on managed cloud infrastructure |
| IoT-to-cloud | Simulator/ESP32 posts telemetry |
| SaaS | Dashboard is a remotely accessible software service |
| PaaS | Render-style managed application hosting runs FastAPI/React without managing servers |
| IaaS | Enterprise AWS EC2/VPC could host the same containers, but it is not required for the student build |
| Cloud database | Supabase managed PostgreSQL |
| Time-series data | `sensor_readings(device_id,timestamp,...)` |
| REST API | `/api/sensors/data`, devices, alerts and watering endpoints |
| MQTT concept | Documented alternative for device telemetry; HTTPS is used in the base build to stay beginner-friendly |
| Serverless | Enterprise variant can move ingestion/automation to Lambda/Functions |
| Cloud Functions | AWS Lambda/Azure Functions/GCP Cloud Functions equivalent |
| Event-driven architecture | A sensor event triggers persistence, rule evaluation and WebSocket broadcast |
| Scalability | Stateless API + managed DB + broker/serverless option |
| Elasticity | Managed/serverless compute can scale horizontally |
| Availability | Managed cloud services, health checks and reconnect/retry patterns |
| Authentication | JWT for dashboard users; separate ingestion key for simulator |
| Authorization | Device queries are restricted to the authenticated user's devices |
| API gateway | Enterprise AWS API Gateway can front Lambda; the student build exposes FastAPI directly behind TLS hosting |
| Load balancing | Cloud PaaS/load balancer distributes requests when scaled |
| Environment variables | `.env` / hosting environment settings |
| Secrets management | Secrets stay outside Git; production should use a managed secret store |
| Logging | Uvicorn/Python simulator logs and platform logs |
| Monitoring | Health endpoint + cloud platform logs; enterprise CloudWatch/Azure Monitor/Cloud Monitoring |
| Alerts | Database alert records; optional email/SMS/push integrations |
| CI/CD | Git push -> connected deployment platform build/deploy |
| Cloud deployment | Render/Supabase or equivalent |

## SaaS/PaaS/IaaS distinction
This project is primarily a **PaaS + managed database** demonstration. The user consumes hosted compute/database services rather than administering physical servers. It can be extended to IaaS by deploying Docker containers on EC2/VMs.

## MQTT
MQTT is useful when thousands of constrained devices publish telemetry through a broker. It is not required for this student implementation because HTTPS REST already demonstrates IoT-to-cloud communication with less infrastructure. An enterprise variant can replace the simulator's POST with MQTT publish while keeping the downstream data model and automation concepts.
