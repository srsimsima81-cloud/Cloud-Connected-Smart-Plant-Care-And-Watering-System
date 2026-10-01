# 🌱 Cloud-Connected Smart Plant Care & Watering System

A cloud-connected IoT application for **real-time plant monitoring, automated watering, alerts, and sensor analytics**. The system simulates IoT sensor readings and sends them to a FastAPI backend, where readings are stored, analyzed, and used to trigger automated watering decisions. A React dashboard provides real-time visibility into plant conditions and watering activity.

> **Project Type:** Cloud Computing + IoT + Full-Stack Application  
> **IoT Hardware:** Python-based sensor simulator with optional ESP32 integration

---

## 📌 Overview

The **Cloud-Connected Smart Plant Care & Watering System** demonstrates how IoT devices can communicate with a cloud-ready backend to monitor plant conditions and automate watering decisions.

The system collects parameters such as:

- 🌱 Soil moisture
- 🌡️ Temperature
- 💧 Humidity
- ☀️ Light level
- 🚰 Water tank level

When soil moisture falls below the configured threshold, the backend can automatically initiate watering while applying safety controls such as watering duration, cooldown periods, and minimum tank-level checks.

The application also maintains sensor history, watering events, alerts, and analytics for monitoring plant health over time.

---

## ✨ Key Features

### 🌿 Real-Time Plant Monitoring
- Live soil moisture monitoring
- Temperature and humidity tracking
- Light-level monitoring
- Water-tank monitoring
- Device online/offline status
- Plant health status

### 💧 Automated Watering
- Configurable soil-moisture threshold
- Automatic watering mode
- Manual watering control
- Maximum watering duration
- Watering cooldown
- Minimum water-tank protection
- Persistent watering event history

### 🚨 Alert System
The system generates alerts for conditions such as:

- Low soil moisture
- High temperature
- Low humidity
- Low water-tank level
- Device/sensor offline status

Alerts are stored and displayed through the dashboard.

### 📊 Analytics
- Average soil moisture
- Minimum and maximum moisture
- Average temperature
- Average humidity
- Watering-event statistics
- Historical sensor charts

### 🔐 Authentication & Device Management
- User registration and authentication
- JWT-based authentication
- Device ownership
- Protected API endpoints
- Configurable plant profiles and thresholds

### 📡 IoT Sensor Simulation
A Python simulator provides controlled sensor scenarios without requiring physical hardware.

Supported scenarios:

```text
normal
low-moisture
high-temperature
low-humidity
low-tank
```

The simulator supports configurable intervals, reproducible test conditions, API retries, and device-specific readings.

---

## 🏗️ System Architecture

```text
┌──────────────────────────┐
│ Python IoT Sensor        │
│ Simulator                │
│                          │
│ Soil / Temp / Humidity   │
│ Light / Tank Level       │
└────────────┬─────────────┘
             │
             │ HTTPS REST API
             ▼
┌──────────────────────────┐
│ FastAPI Backend          │
│                          │
│ Authentication           │
│ Device Management        │
│ Sensor Ingestion         │
│ Automation Logic        │
│ Alerts                   │
│ Analytics                │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ PostgreSQL Database      │
│                          │
│ Users                    │
│ Devices                  │
│ Sensor Readings          │
│ Watering Events          │
│ Alerts                   │
└──────────────────────────┘
             ▲
             │
             │ REST / WebSocket
             │
┌────────────┴─────────────┐
│ React Dashboard          │
│                          │
│ Live Monitoring          │
│ Charts & Analytics       │
│ Alerts                   │
│ Watering Controls        │
└──────────────────────────┘
```

---

## 🛠️ Technology Stack

### Frontend
- React
- Vite
- JavaScript
- Recharts
- WebSocket-based updates

### Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- REST APIs

### Database
- PostgreSQL
- Supabase PostgreSQL supported for cloud deployment

### IoT / Simulation
- Python
- HTTP/REST communication
- Optional ESP32 integration

### Infrastructure
- Docker
- Docker Compose
- Environment-based configuration

---

## ☁️ Cloud Computing Concepts Demonstrated

This project demonstrates several concepts commonly associated with cloud-based IoT applications:

| Concept | Implementation |
|---|---|
| Cloud-ready architecture | Separated frontend, backend, and database |
| IoT-to-cloud communication | Sensor simulator sends readings to backend APIs |
| Cloud database | PostgreSQL / Supabase PostgreSQL support |
| REST API | FastAPI sensor and device APIs |
| Authentication | JWT-based authentication |
| Authorization | User/device ownership |
| Event-driven behavior | Sensor conditions trigger watering and alerts |
| Monitoring | Sensor history and device status |
| Alerting | Stored condition-based alerts |
| Scalability | Stateless API-oriented architecture |
| Containerization | Docker and Docker Compose |
| Environment configuration | `.env` based configuration |
| WebSocket communication | Real-time dashboard updates |

---

## 📂 Project Structure

```text
Cloud-Connected-Smart-Plant-Care-And-Watering-System/
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── sensor_simulator/
│   ├── simulator.py
│   ├── config.py
│   └── requirements.txt
│
├── esp32/
│   └── optional ESP32 integration
│
├── docs/
│   ├── architecture
│   ├── testing
│   └── project documentation
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Running the Project

### Prerequisites

Install:

- Python 3.11+
- Node.js
- Docker Desktop
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/srsimsima81-cloud/Cloud-Connected-Smart-Plant-Care-And-Watering-System.git
cd Cloud-Connected-Smart-Plant-Care-And-Watering-System
```

---

### 2. Configure Environment Variables

Create the required environment files using the provided examples.

Do **not** commit real passwords, JWT secrets, API keys, or other credentials to GitHub.

---

### 3. Start the Backend

Using Docker Compose:

```bash
docker compose up --build
```

The FastAPI backend will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

### 4. Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open the local Vite URL shown in the terminal.

---

### 5. Start the IoT Simulator

Open another terminal:

```bash
cd sensor_simulator
```

Run a normal monitoring scenario:

```bash
py simulator.py --device-id PLANT-001 --scenario normal --interval 5
```

Low-moisture scenario:

```bash
py simulator.py --device-id PLANT-001 --scenario low-moisture --interval 5
```

Other available scenarios:

```text
high-temperature
low-humidity
low-tank
```

---

## 🧪 Demonstration Scenarios

### Scenario 1 — Healthy Monitoring

The normal simulator maintains soil moisture within a healthy range.

Expected behavior:

```text
Device → Online
Plant → Healthy
Pump → OFF
```

The dashboard displays live sensor readings, charts, and analytics.

### Scenario 2 — Low Moisture & Automated Watering

The low-moisture scenario introduces a soil-moisture condition below the configured threshold.

Expected behavior:

```text
Low Moisture
      ↓
Warning Alert
      ↓
Automatic Watering
      ↓
Watering Event Recorded
```

The dashboard displays the alert, pump state, sensor readings, and watering history.

---


## 🔌 API Overview

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/sensors/data` | Submit sensor readings |
| GET | `/api/devices` | List user devices |
| POST | `/api/devices` | Create a device |
| GET | `/api/devices/{id}` | Get device details |
| GET | `/api/devices/{id}/latest` | Get latest sensor data |
| GET | `/api/devices/{id}/history` | Get sensor history |
| PUT | `/api/devices/{id}/threshold` | Update moisture threshold |
| POST | `/api/devices/{id}/water` | Trigger manual watering |
| GET | `/api/devices/{id}/watering-history` | View watering events |
| GET | `/api/devices/{id}/alerts` | View alerts |
| PUT | `/api/alerts/{id}/acknowledge` | Acknowledge an alert |

Full interactive API documentation is available through FastAPI Swagger UI at `/docs`.

---

## 🔒 Security Considerations

The project includes several basic application-security practices:

- JWT-based authentication
- Password hashing
- Protected API endpoints
- Device ownership checks
- Environment-based secrets
- Simulator API-key protection
- Input validation
- Duplicate-reading protection
- Separation of configuration from source code

Sensitive credentials should always remain in environment variables and should never be committed to the repository.

---

## 🧩 Reliability & Failure Handling

The system includes handling for common IoT/cloud application conditions:

- API communication failures
- Sensor data retries
- Duplicate sensor readings
- Offline devices
- Low water-tank conditions
- Watering cooldowns
- Maximum watering duration
- Invalid sensor input
- Authentication failures

These mechanisms help demonstrate how a cloud-connected IoT system can continue operating safely under common failure conditions.

---

## 📈 Future Enhancements

Possible future improvements include:

- MQTT-based IoT communication
- Physical ESP32 deployment
- Cloud-hosted frontend and backend
- Serverless automation functions
- Push notifications
- Email notifications
- Mobile application
- Multiple plant-location support
- Advanced plant-specific prediction models
- Time-series database integration
- Cloud monitoring and observability
- CI/CD deployment pipelines

---

## 🎓 Academic & Learning Objectives

This project was developed to demonstrate practical understanding of:

- Cloud computing
- Internet of Things
- REST API development
- Full-stack application development
- Database design
- Authentication and authorization
- Event-driven automation
- Real-time monitoring
- Containerization
- Sensor-data processing
- Cloud-ready system architecture

---
