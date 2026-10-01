# Three Implementation Options

| Option | Stack | Difficulty | Cost | Hardware | Cloud concepts | Output |
|---|---|---|---|---|---|---|
| A | Python simulator + FastAPI + React/HTML + SQLite + REST | Beginner | Free/local | None | API, DB, local simulation | Fully local demo |
| B | Python simulator + FastAPI + React + Supabase Postgres + REST/WebSocket | Recommended student cloud | Free-tier where available | None | managed DB, PaaS, auth, deployment, realtime, APIs | Cloud-deployed proof of work |
| C | ESP32 + sensors + MQTT/HTTPS + AWS IoT/Azure/GCP + managed/time-series DB | Advanced | Free tiers/credits vary | ESP32, sensors, relay/pump | IoT broker, serverless, queues, time-series, monitoring | Hardware + enterprise cloud |

## Recommendation
For a student without hardware, use **Option B**. It preserves the strongest cloud-computing story without requiring physical electronics. Keep Option A as the local fallback and Option C as the documented future/hardware extension.
