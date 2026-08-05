# Security & Authentication Policies

## Authentication
- JWT Bearer Tokens using standard HS256 algorithm with configurable expiration.
- Password hashing powered by Passlib.

## Security Practices
- Parameterized SQL execution preventing SQL injection.
- Centralized payload sanitization stripping potential HTML/Script tags.
- Rate-limiting headers and correlation ID tracking on all routes.
