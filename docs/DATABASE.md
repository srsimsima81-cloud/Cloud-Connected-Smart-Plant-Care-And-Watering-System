# Database Design

## USERS
`user_id` PK, `name`, `email` unique, `password_hash`, `created_at`.

## DEVICES
`device_id` PK, `user_id` FK, `plant_name`, `plant_type`, `location`, `moisture_threshold`, `temperature_threshold`, `humidity_minimum`, `tank_minimum`, `watering_duration`, `cooldown_seconds`, `auto_water`, `pump_on`, `pump_started_at`, `last_seen`, `created_at`.

## SENSOR_READINGS
`reading_id` PK, `device_id` FK, soil moisture, temperature, humidity, light, tank level, timestamp, `reading_key` unique per device. Indexes exist on `(device_id,timestamp)` and device ID.

## WATERING_EVENTS
`event_id` PK, `device_id` FK, trigger type, moisture before/after, duration, timestamp, status.

## ALERTS
`alert_id` PK, `device_id` FK, alert type, severity, message, status, timestamps.

## Relationships
`User 1 -> many Devices -> many SensorReadings / WateringEvents / Alerts`.

For a larger deployment, partition high-volume readings by time/device, use connection pooling, retention policies and a time-series store where appropriate.
