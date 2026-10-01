# Scalability

### 10 plants
A single FastAPI instance and PostgreSQL database are enough. REST polling/WebSocket is simple and inexpensive.

### 1,000 plants
Use managed PostgreSQL indexes, connection pooling, API horizontal scaling, rate limiting and a queue/broker for bursts. Store only required telemetry at high frequency.

### 100,000 plants
Use an IoT broker such as AWS IoT Core, MQTT, partitioned/event-driven ingestion, serverless consumers, time-series optimized storage, object storage for long-term history, caching and retention/downsampling policies.

### 1,000,000+ readings
Batch/stream ingestion, partition by device/time, asynchronous processing, compression/downsampling, hot/cold storage tiers and analytical warehouses become important.

If thousands of devices publish simultaneously, a broker/queue absorbs bursts. Consumers process messages asynchronously so the database is not overwhelmed by direct synchronized writes from every device.
