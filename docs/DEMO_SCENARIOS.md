# Reproducible Demo Scenarios

Create `PLANT-001` with moisture threshold 30%, auto watering enabled, tank minimum 15%, watering duration 5 seconds and cooldown 30 seconds.

## Normal
`py sensor_simulator/simulator.py --device-id PLANT-001 --scenario normal --interval 5`
Expected: healthy telemetry, no watering while moisture remains above threshold.

## Automatic watering
`py sensor_simulator/simulator.py --device-id PLANT-001 --scenario low-moisture --interval 5`
Expected: moisture falls below 30%, WARNING alert appears, backend sets virtual pump ON, watering event is stored, simulator models increasing moisture, pump later turns OFF.

## High temperature
`py sensor_simulator/simulator.py --device-id PLANT-001 --scenario high-temperature --interval 5`
Expected: HIGH_TEMPERATURE warning.

## Low humidity
`py sensor_simulator/simulator.py --device-id PLANT-001 --scenario low-humidity --interval 5`
Expected: LOW_HUMIDITY info alert.

## Low tank
`py sensor_simulator/simulator.py --device-id PLANT-001 --scenario low-tank --interval 5`
Expected: CRITICAL low-tank alert; automatic watering is blocked if the configured minimum is higher than the reported tank level.

## Offline/recovery
Stop the simulator with Ctrl+C and wait longer than `OFFLINE_AFTER_SECONDS`. The backend creates a DEVICE_OFFLINE critical alert. Restart the simulator; the backend resolves the offline alert and creates a DEVICE_RECOVERED info alert.

## Manual watering
Click **Manual Water** while the pump is OFF. The backend records `trigger_type=manual`; it is not merely a frontend label change.
