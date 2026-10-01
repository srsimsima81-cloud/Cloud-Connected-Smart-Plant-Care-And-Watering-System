def device_dict(d):
    return {'device_id': d.device_id, 'plant_name': d.plant_name, 'plant_type': d.plant_type, 'location': d.location,
            'moisture_threshold': d.moisture_threshold, 'temperature_threshold': d.temperature_threshold,
            'humidity_minimum': d.humidity_minimum, 'tank_minimum': d.tank_minimum, 'watering_duration': d.watering_duration,
            'cooldown_seconds': d.cooldown_seconds, 'auto_water': d.auto_water, 'pump_on': d.pump_on,
            'pump_started_at': d.pump_started_at, 'last_seen': d.last_seen}
def reading_dict(r):
    return {'reading_id': r.reading_id, 'device_id': r.device_id, 'soil_moisture': r.soil_moisture, 'temperature': r.temperature,
            'humidity': r.humidity, 'light_level': r.light_level, 'water_tank_level': r.water_tank_level, 'timestamp': r.timestamp}
def event_dict(e):
    return {'event_id': e.event_id, 'device_id': e.device_id, 'trigger_type': e.trigger_type, 'moisture_before': e.moisture_before,
            'moisture_after': e.moisture_after, 'duration': e.duration, 'timestamp': e.timestamp, 'status': e.status}
def alert_dict(a):
    return {'alert_id': a.alert_id, 'device_id': a.device_id, 'alert_type': a.alert_type, 'level': a.level, 'message': a.message,
            'status': a.status, 'created_at': a.created_at, 'acknowledged_at': a.acknowledged_at}
