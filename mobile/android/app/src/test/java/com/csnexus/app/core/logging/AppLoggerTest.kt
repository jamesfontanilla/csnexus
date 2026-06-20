package com.csnexus.app.core.logging

import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class AppLoggerTest {
    @Test
    fun redactsSensitiveValues() {
        val redacted = redactSensitive(
            "access_token=abc refresh_token=def password=secret otp=123456 code=999999",
        )

        assertTrue(redacted.contains("access_token=<redacted>"))
        assertTrue(redacted.contains("refresh_token=<redacted>"))
        assertTrue(redacted.contains("password=<redacted>"))
        assertTrue(redacted.contains("otp=<redacted>"))
        assertTrue(redacted.contains("code=<redacted>"))
        assertFalse(redacted.contains("abc"))
        assertFalse(redacted.contains("def"))
        assertFalse(redacted.contains("secret"))
        assertFalse(redacted.contains("123456"))
    }

    @Test
    fun redactsJsonSensitiveValues() {
        val redacted = redactSensitive(
            """{"access_token":"abc","refresh_token":"def","password":"secret","otp":"123456"}""",
        )

        assertTrue(redacted.contains(""""access_token":"<redacted>""""))
        assertTrue(redacted.contains(""""refresh_token":"<redacted>""""))
        assertFalse(redacted.contains("abc"))
        assertFalse(redacted.contains("def"))
        assertFalse(redacted.contains("secret"))
        assertFalse(redacted.contains("123456"))
    }

    @Test
    fun redactsAuthorizationAndProfileSensitiveValues() {
        val redacted = redactSensitive(
            """Authorization: Bearer abc123 email=learner@example.com display_name=Jamie username=learner""",
        )

        assertTrue(redacted.contains("Authorization: Bearer <redacted>"))
        assertTrue(redacted.contains("email=<redacted>"))
        assertTrue(redacted.contains("display_name=<redacted>"))
        assertTrue(redacted.contains("username=<redacted>"))
        assertFalse(redacted.contains("abc123"))
        assertFalse(redacted.contains("learner@example.com"))
        assertFalse(redacted.contains("Jamie"))
        assertFalse(redacted.contains("learner"))
    }

    @Test
    fun formatDiagnosticLogRedactsStructuredSensitiveExtras() {
        val rendered = formatDiagnosticLog(
            event = "auth_login_failure",
            context = DiagnosticsContext(
                screenName = "Login",
                endpoint = "v1/auth/sessions",
                requestId = "req-1",
                statusClass = "4xx",
                extras = mapOf(
                    "email" to "learner@example.com",
                    "password" to "Password1!",
                    "error_code" to "INVALID_CREDENTIALS",
                ),
            ),
            message = "Password rejected",
        )

        assertTrue(rendered.contains("event=auth_login_failure"))
        assertTrue(rendered.contains("screen=Login"))
        assertTrue(rendered.contains("endpoint=v1/auth/sessions"))
        assertTrue(rendered.contains("request_id=req-1"))
        assertTrue(rendered.contains("status_class=4xx"))
        assertTrue(rendered.contains("email=<redacted>"))
        assertTrue(rendered.contains("password=<redacted>"))
        assertTrue(rendered.contains("error_code=INVALID_CREDENTIALS"))
        assertFalse(rendered.contains("learner@example.com"))
        assertFalse(rendered.contains("Password1!"))
    }
}
