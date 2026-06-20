package com.csnexus.app.core.network

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Test

class ApiErrorMapperTest {
    @Test
    fun decodesBackendErrorEnvelope() {
        val envelope = ApiErrorMapper.decodeErrorEnvelope(
            """{"error":{"message":"Invalid credentials","code":"INVALID_CREDENTIALS"}}""",
        )

        assertNotNull(envelope)
        assertEquals("Invalid credentials", envelope?.error?.message)
        assertEquals("INVALID_CREDENTIALS", envelope?.error?.code)
    }

    @Test
    fun decodesPlainDetailEnvelope() {
        val envelope = ApiErrorMapper.decodeErrorEnvelope(
            """{"detail":"invalid_credentials"}""",
        )

        assertNotNull(envelope)
        assertEquals("invalid_credentials", envelope?.detail)
    }
}
