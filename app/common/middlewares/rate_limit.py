"""HTTP-level rate limiting for auth-sensitive endpoints.

Uses ``slowapi`` (a Starlette/FastAPI wrapper around ``limits``) to enforce
per-IP request caps on endpoints that are attractive to credential-stuffing
and brute-force attacks.

Two limiters are exposed:

* ``auth_limiter`` — strict limit for login, signup, password-reset, and OTP
  endpoints (10 requests per minute per IP). This sits above the per-user
  lockout logic in the auth service and prevents an attacker from rotating
  across a list of emails at high speed.
* ``default_limiter`` — lenient global fallback (120 requests per minute per
  IP) applied at the app level to prevent general abuse.

The limiters key on the client IP extracted from ``X-Forwarded-For`` when
behind a reverse proxy, falling back to the direct connection IP.

Integration:
    Import ``limiter`` in ``main.py`` and attach the ``SlowAPIMiddleware``.
    Import ``auth_rate_limit`` in auth/otp routers and apply as a dependency.
"""

from __future__ import annotations

from slowapi import Limiter
from slowapi.util import get_remote_address

# Key function: uses X-Forwarded-For if present, else direct IP.
limiter = Limiter(key_func=get_remote_address)

# Dependency-style rate limit strings for use in route decorators.
AUTH_RATE_LIMIT: str = "10/minute"
DEFAULT_RATE_LIMIT: str = "120/minute"
