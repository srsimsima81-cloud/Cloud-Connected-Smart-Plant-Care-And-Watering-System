# REST API Reference

All dashboard endpoints require `Authorization: Bearer <JWT>`. Sensor ingestion and device control-state use `X-Simulator-Key`.

| Method | Endpoint | Purpose | Typical success |
|---|---|---|---|
| POST | `/api/auth/register` | create user | 201 + token |
| POST | `/api/auth/login` | authenticate | 200 + token |
| POST | `/api/sensors/data` | ingest telemetry | 200 |
| GET | `/api/devices` | list user's devices | 200 |
| POST | `/api/devices` | create device | 201 |
| GET | `/api/devices/{id}` | device config/status | 200 |
| GET | `/api/devices/{id}/latest` | latest reading | 200 |
| GET | `/api/devices/{id}/history` | historical readings | 200 |
| PUT | `/api/devices/{id}/threshold` | change thresholds/auto mode | 200 |
| POST | `/api/devices/{id}/water` | manual watering | 200 |
| GET | `/api/devices/{id}/watering-history` | watering events | 200 |
| GET | `/api/devices/{id}/control-state` | device actuator state | 200 |
| GET | `/api/alerts` | current user's alerts | 200 |
| PUT | `/api/alerts/{id}/acknowledge` | acknowledge alert | 200 |
| GET | `/api/analytics/{id}` | telemetry analytics | 200 |
| GET | `/health` | service health | 200 |
| WS | `/ws` | near-real-time dashboard events | WebSocket |

## Sensor request
```json
{
  "device_id":"PLANT-001",
  "soil_moisture":32,
  "temperature":29.4,
  "humidity":61,
  "light_level":72,
  "water_tank_level":85,
  "timestamp":"2026-09-30T16:00:00Z",
  "reading_key":"PLANT-001-demo-001"
}
```

## Authentication/validation/error codes
- `200`: successful request
- `201`: resource created
- `401`: missing/invalid authentication
- `404`: resource/device not found
- `409`: duplicate device or conflicting actuator operation
- `422`: schema/range validation failure
- `500`: unexpected server error

## Watering decision
`soil < threshold AND auto_water AND tank >= minimum AND pump OFF AND cooldown elapsed -> pump ON -> watering event created`.

The maintenance loop later turns the virtual pump off after the configured maximum duration.
