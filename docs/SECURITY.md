# Security Notes

- User passwords are bcrypt-hashed; plaintext passwords are never stored.
- Dashboard API access uses short-lived JWTs.
- Simulator/device ingestion uses a separate secret header so device telemetry is not an unauthenticated public write endpoint.
- Device ownership is checked on dashboard endpoints.
- Pydantic validates ranges and required fields.
- Duplicate reading keys are rejected by a database uniqueness constraint.
- Use HTTPS/TLS in cloud deployments. Do not expose a raw HTTP control API publicly.
- Store JWT secrets, database passwords and device keys in hosting environment variables or a managed secrets service.
- Production should add rate limiting, key rotation, per-device certificates/credentials, audit logs, database least-privilege roles, backups, migrations, CSRF-aware browser patterns where applicable, and stricter CORS.

## Why a public pump endpoint is dangerous
An unauthenticated actuator endpoint could allow anyone who discovers the URL to repeatedly activate a pump, waste water, damage plants/equipment, or create denial-of-service conditions. In real deployments, commands should require authenticated identities, authorization, validation, rate limits, audit logging and safe actuator limits.
