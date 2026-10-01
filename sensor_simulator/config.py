import os
API_URL=os.getenv('API_URL','http://127.0.0.1:8000')
DEVICE_ID=os.getenv('DEVICE_ID','')
SIMULATOR_API_KEY=os.getenv('SIMULATOR_API_KEY','local-simulator-key')
INTERVAL=float(os.getenv('INTERVAL','5'))
SCENARIO=os.getenv('SCENARIO','normal')
