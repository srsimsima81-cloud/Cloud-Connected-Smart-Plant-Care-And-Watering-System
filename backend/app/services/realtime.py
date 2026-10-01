from typing import Set
from fastapi import WebSocket
class ConnectionManager:
    def __init__(self): self.connections: Set[WebSocket] = set()
    async def connect(self, ws): await ws.accept(); self.connections.add(ws)
    def disconnect(self, ws): self.connections.discard(ws)
    async def broadcast(self, payload):
        dead=[]
        for ws in list(self.connections):
            try: await ws.send_json(payload)
            except Exception: dead.append(ws)
        for ws in dead: self.disconnect(ws)
manager = ConnectionManager()
