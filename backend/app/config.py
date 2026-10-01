import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv('DATABASE_URL', 'sqlite:///./plantcare.db')
    jwt_secret: str = os.getenv('JWT_SECRET', 'change-me-in-production')
    jwt_exp_minutes: int = int(os.getenv('JWT_EXP_MINUTES', '120'))
    cors_origins: str = os.getenv('CORS_ORIGINS', 'http://localhost:5173')
    offline_after_seconds: int = int(os.getenv('OFFLINE_AFTER_SECONDS', '30'))
    simulator_api_key: str = os.getenv('SIMULATOR_API_KEY', 'local-simulator-key')

settings = Settings()
