PLANT_PROFILES = {
    'SUCCULENT': 20,
    'TOMATO': 40,
    'HERB': 35,
    'INDOOR PLANT': 30,
}

def threshold_for(plant_type: str) -> float:
    return PLANT_PROFILES.get(plant_type.upper(), 30)
