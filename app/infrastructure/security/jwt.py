"""HS256 access-token and refresh-token encoding and decoding.

The signing secret is read lazily from the ``JWT_SECRET`` environment variable
on every encode/decode. Reading it lazily (rather than at module import) lets
tests use ``monkeypatch.setenv`` and lets the deploy environment populate the
secret after the process starts.

Callers are responsible for translating ``pyjwt`` exceptions
(``ExpiredSignatureError``, ``InvalidSignatureError``, ``InvalidTokenError``,
etc.) into HTTP 401 responses. We deliberately do not wrap them in custom
exceptions: the ``pyjwt`` hierarchy is the one downstream code already knows.
"""

from __future__ import annotations

import os
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Final

import jwt

JWT_ALGORITHM: Final[str] = "HS256"
ACCESS_TOKEN_TYPE: Final[str] = "access"
REFRESH_TOKEN_TYPE: Final[str] = "refresh"
JWT_ACCESS_TTL_SECONDS: Final[int] = int(
    os.environ.get("JWT_ACCESS_TTL_SECONDS", "900")
)
JWT_REFRESH_TTL_SECONDS: Final[int] = int(
    os.environ.get("JWT_REFRESH_TTL_SECONDS", "2592000")
)
_JWT_SECRET_ENV: Final[str] = "JWT_SECRET"


def _secret() -> str:
    secret = os.environ.get(_JWT_SECRET_ENV)
    if not secret:
        raise RuntimeError(
            f"{_JWT_SECRET_ENV} environment variable is not set. "
            "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    return secret


def encode_token(
    *,
    sub: str | int,
    jti: str | None = None,
    token_type: str = ACCESS_TOKEN_TYPE,
    ttl_seconds: int | None = None,
) -> tuple[str, dict[str, Any]]:
    """Mint a fresh JWT for the given subject.

    Returns:
        ``(token, claims)`` where ``claims`` is the dict that was signed, so
        callers (e.g., the auth service persisting a session row) can record
        ``jti`` / ``iat`` / ``exp`` without a redundant decode.
    """
    now = datetime.now(tz=timezone.utc)
    iat = int(now.timestamp())
    effective_ttl = ttl_seconds or _default_ttl_seconds(token_type)
    exp = iat + effective_ttl
    claims: dict[str, Any] = {
        "sub": str(sub),
        "jti": jti if jti is not None else str(uuid.uuid4()),
        "iat": iat,
        "exp": exp,
        "typ": token_type,
    }
    token = jwt.encode(claims, _secret(), algorithm=JWT_ALGORITHM)
    return token, claims


def decode_token(token: str, *, expected_type: str | None = None) -> dict[str, Any]:
    """Decode and verify ``token``.

    Lets ``pyjwt`` raise its own exceptions on failure: ``ExpiredSignatureError``
    on stale tokens, ``InvalidSignatureError`` on tampered signatures, and the
    broader ``InvalidTokenError`` family on structural problems.
    """
    claims = jwt.decode(token, _secret(), algorithms=[JWT_ALGORITHM])
    token_type = claims.get("typ")
    if expected_type is not None:
        # Backward compatibility: older access tokens in the field may not
        # carry a `typ` claim yet, so treat a missing type as `access`.
        if not (
            token_type == expected_type
            or (token_type is None and expected_type == ACCESS_TOKEN_TYPE)
        ):
            raise jwt.InvalidTokenError("unexpected_token_type")
    return claims


def _default_ttl_seconds(token_type: str) -> int:
    if token_type == ACCESS_TOKEN_TYPE:
        return JWT_ACCESS_TTL_SECONDS
    if token_type == REFRESH_TOKEN_TYPE:
        return JWT_REFRESH_TTL_SECONDS
    raise ValueError(f"Unsupported token type: {token_type}")
