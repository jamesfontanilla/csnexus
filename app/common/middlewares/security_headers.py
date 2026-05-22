"""Security headers middleware.

Adds standard security headers to every response:

* ``Strict-Transport-Security`` — instructs browsers to only connect via
  HTTPS for the next year (with subdomains). Only emitted when the app
  detects it is running behind HTTPS (``APP_ENV=production``).
* ``X-Content-Type-Options: nosniff`` — prevents MIME-type sniffing.
* ``X-Frame-Options: DENY`` — prevents clickjacking via iframes.
* ``Referrer-Policy: strict-origin-when-cross-origin`` — limits referrer
  leakage on cross-origin navigations.
* ``Permissions-Policy`` — disables camera, microphone, geolocation by
  default (not needed for an educational platform).
* ``Cache-Control: no-store`` — prevents caching of authenticated API
  responses. Individual endpoints that serve public/static content can
  override this header.

These headers are defense-in-depth; they do not replace proper HTTPS
termination at the reverse proxy / CDN layer.
"""

from __future__ import annotations

import os

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

_IS_PRODUCTION: bool = os.environ.get("APP_ENV", "development") == "production"


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Append security headers to every response."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        if _IS_PRODUCTION:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )
        response.headers["Cache-Control"] = "no-store"

        return response
