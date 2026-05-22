"""Brevo-backed OTP email delivery adapter.

Sends transactional email via the Brevo API (https://brevo.com) using
only Python's stdlib ``urllib`` — no extra dependency required.

Free tier: 300 emails/day (~9,000/month). Sufficient for ~2,000+ active
users doing OTP and password-reset flows.

Configuration (environment variables):
    BREVO_API_KEY    — required for live sending (get from Brevo dashboard)
    EMAIL_FROM_ADDR  — sender address, must be a verified Brevo sender/domain
                       (default: "CSNexus <noreply@csnexus.space>")

When ``BREVO_API_KEY`` is unset the adapter is a no-op that logs a warning
and returns ``False``, so local dev and tests work without credentials.

Security note (security-policy.md): the OTP code is sent in the email body
but is NOT logged anywhere in this module. The structured log line emitted
on success/failure contains only the recipient address and purpose.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Final

from app.infrastructure.external.base import ExternalServiceBase

logger = logging.getLogger(__name__)

_BREVO_API_URL: Final[str] = "https://api.brevo.com/v3/smtp/email"


class SmtpOtpSender(ExternalServiceBase):
    """Adapter that delivers OTP codes via the Brevo transactional email API.

    The class is named ``SmtpOtpSender`` to preserve the existing injection
    surface — all call sites use this name and no rename is needed.

    Constructor arguments default to environment variables when ``None`` is
    passed, matching the constructor-injection convention from
    ``ExternalServiceBase``. Tests can override every value without touching
    ``os.environ``.
    """

    def __init__(
        self,
        api_key: str | None = None,
        from_addr: str | None = None,
    ) -> None:
        self.api_key = (
            api_key if api_key is not None else os.environ.get("BREVO_API_KEY", "")
        )
        self.from_addr = (
            from_addr
            if from_addr is not None
            else os.environ.get("EMAIL_FROM_ADDR", "CSNexus <noreply@csnexus.space>")
        )

    # ------------------------------------------------------------------
    # public surface
    # ------------------------------------------------------------------

    def send_otp(self, to_email: str, code: str, purpose: str) -> bool:
        """Send the OTP ``code`` to ``to_email`` via Brevo.

        Returns ``True`` on success, ``False`` on any failure (missing key,
        network error, API error). Logs errors but does not raise so the
        caller can fall back to offline delivery.

        The ``code`` value is intentionally NOT included in any log line
        (Req 21.3 redaction policy).
        """
        if not self.api_key:
            logger.warning(
                "brevo_otp_sender.skipped: BREVO_API_KEY not set",
                extra={"to_email": to_email, "purpose": purpose},
            )
            return False

        subject, body = self._build_message(code, purpose)

        # Parse "Display Name <email>" format for Brevo's sender object
        sender_name, sender_email = self._parse_from_addr(self.from_addr)

        payload = json.dumps(
            {
                "sender": {"name": sender_name, "email": sender_email},
                "to": [{"email": to_email}],
                "subject": subject,
                "textContent": body,
            }
        ).encode("utf-8")

        req = urllib.request.Request(
            _BREVO_API_URL,
            data=payload,
            headers={
                "api-key": self.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.status
            if status in (200, 201):
                logger.info(
                    "brevo_otp_sender.sent",
                    extra={"to_email": to_email, "purpose": purpose},
                )
                return True
            logger.error(
                "brevo_otp_sender.unexpected_status: %s",
                status,
                extra={"to_email": to_email, "purpose": purpose},
            )
            return False
        except urllib.error.HTTPError as exc:
            logger.error(
                "brevo_otp_sender.http_error: %s %s",
                exc.code,
                exc.reason,
                extra={"to_email": to_email, "purpose": purpose},
            )
            return False
        except Exception as exc:
            logger.error(
                "brevo_otp_sender.failed: %s",
                str(exc),
                extra={"to_email": to_email, "purpose": purpose},
            )
            return False

    def health_check(self) -> bool:
        """Return True iff a Brevo API key is configured."""
        return bool(self.api_key)

    # ------------------------------------------------------------------
    # private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_from_addr(from_addr: str) -> tuple[str, str]:
        """Parse 'Display Name <email>' into (name, email) tuple."""
        if "<" in from_addr and ">" in from_addr:
            name = from_addr.split("<")[0].strip()
            email = from_addr.split("<")[1].rstrip(">").strip()
            return name, email
        return "CSNexus", from_addr

    @staticmethod
    def _build_message(code: str, purpose: str) -> tuple[str, str]:
        """Return ``(subject, plain-text body)`` for the given purpose."""
        if purpose == "VERIFY_EMAIL":
            purpose_label = "email verification"
        else:
            purpose_label = "password reset"

        subject = f"CSNexus — Your {purpose_label} code"
        body = (
            f"Your CSNexus {purpose_label} code is:\n\n"
            f"    {code}\n\n"
            f"This code expires in 5 minutes. Do not share it with anyone.\n\n"
            f"If you didn't request this, you can safely ignore this email."
        )
        return subject, body
