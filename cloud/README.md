# Cloud Layer

The project uses a provider-neutral database URL. Local development uses SQLite; cloud deployment uses managed PostgreSQL such as Supabase. `database_service.py` is intentionally not required because SQLAlchemy provides the database abstraction used by the backend.

Enterprise mapping is documented in `../docs/DEPLOYMENT.md`:
AWS IoT Core/API Gateway -> Lambda -> DynamoDB/Timestream -> SNS -> S3/CloudFront -> CloudWatch.
