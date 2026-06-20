package com.csnexus.app.core.contracts

import com.csnexus.app.feature.auth.data.LoginResponseDto
import com.csnexus.app.feature.tutor.data.LessonChatHistoryItemDto
import com.csnexus.app.feature.tutor.data.LessonChatRequestDto
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.encodeToJsonElement
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class ApiContractFixtureTest {
    private val json = Json { ignoreUnknownKeys = true }

    @Test
    fun refreshSuccessFixtureMatchesLoginResponseContract() {
        val fixture = fixture("auth-refresh-success.json")
        val request = fixture["request"]!!.jsonObject
        val response = fixture["response"]!!.jsonObject
        val body = response["body"]!!.jsonObject
        val decoded = json.decodeFromJsonElement(LoginResponseDto.serializer(), body)

        assertEquals("POST", request.string("method"))
        assertEquals("/v1/auth/sessions:refresh", request.string("path"))
        assertEquals("refresh-token-current", request["body"]!!.jsonObject.string("refresh_token"))
        assertEquals(200, response.int("status"))
        assertEquals("access-token-new", decoded.accessToken)
        assertEquals("refresh-token-current", decoded.refreshToken)
        assertEquals(900, decoded.expiresIn)
        assertEquals(2_592_000, decoded.refreshExpiresIn)
    }

    @Test
    fun refreshRotatedFixturePreservesRotatingRefreshTokenShape() {
        val fixture = fixture("auth-refresh-rotated.json")
        val body = fixture["response"]!!.jsonObject["body"]!!.jsonObject
        val decoded = json.decodeFromJsonElement(LoginResponseDto.serializer(), body)

        assertEquals("access-token-new", decoded.accessToken)
        assertEquals("refresh-token-rotated", decoded.refreshToken)
        assertEquals("bearer", decoded.tokenType.lowercase())
    }

    @Test
    fun googleExchangeFixturesDescribeAndroidSpecificContract() {
        val success = fixture("google-exchange-success.json")
        val successRequest = success["request"]!!.jsonObject
        val successResponse = success["response"]!!.jsonObject

        assertEquals("/v1/auth/google", successRequest.string("path"))
        assertEquals("android", successRequest["body"]!!.jsonObject.string("platform"))
        assertEquals("com.csnexus.app", successRequest["body"]!!.jsonObject.string("android_package"))
        assertEquals(200, successResponse.int("status"))
        assertEquals("signed_in", successResponse["body"]!!.jsonObject.string("account_status"))

        val failure = fixture("google-exchange-unverified-email.json")
        val failureResponse = failure["response"]!!.jsonObject
        val error = failureResponse["body"]!!.jsonObject["error"]!!.jsonObject

        assertEquals(403, failureResponse.int("status"))
        assertEquals("GOOGLE_EMAIL_UNVERIFIED", error.string("code"))
        assertTrue(error.string("message").contains("verified", ignoreCase = true))
    }

    @Test
    fun progressSyncFixtureKeepsAcceptedRejectedConflictArraysStable() {
        val fixture = fixture("progress-sync-mixed-response.json")
        val request = fixture["request"]!!.jsonObject
        val responseBody = fixture["response"]!!.jsonObject["body"]!!.jsonObject
        val events = request["body"]!!.jsonObject["events"]!!.jsonArray

        assertEquals("/v1/progress:sync", request.string("path"))
        assertEquals(1, events.size)
        assertEquals("lesson.completed", events.first().jsonObject.string("kind"))
        assertEquals(1, responseBody["accepted"]!!.jsonArray.size)
        assertEquals(1, responseBody["rejected"]!!.jsonArray.size)
        assertEquals(1, responseBody["conflicts"]!!.jsonArray.size)
        assertFalse(
            responseBody["accepted"]!!.jsonArray.first().jsonObject["server_state"]!!
                .jsonObject.isEmpty(),
        )
        assertEquals(
            "invalid_payload",
            responseBody["rejected"]!!.jsonArray.first().jsonObject.string("reason"),
        )
        assertEquals(
            "stale_client_state",
            responseBody["conflicts"]!!.jsonArray.first().jsonObject.string("reason"),
        )
    }

    @Test
    fun tutorLessonChatRequestSerializesStructuredLessonContext() {
        val encoded = json.encodeToJsonElement(
            LessonChatRequestDto.serializer(),
            LessonChatRequestDto(
                message = "Explain this line",
                context = "lesson-42",
                subtopicId = 42,
                activeSectionIndex = 2,
                history = listOf(
                    LessonChatHistoryItemDto(role = "user", content = "Can you explain this?"),
                    LessonChatHistoryItemDto(role = "assistant", content = "Sure."),
                ),
            ),
        ).jsonObject

        assertEquals("Explain this line", encoded.string("message"))
        assertEquals("lesson-42", encoded.string("context"))
        assertEquals(42, encoded.int("subtopic_id"))
        assertEquals(2, encoded.int("active_section_index"))
        assertEquals(2, encoded["history"]!!.jsonArray.size)
        assertEquals("user", encoded["history"]!!.jsonArray.first().jsonObject.string("role"))
        assertEquals("Can you explain this?", encoded["history"]!!.jsonArray.first().jsonObject.string("content"))
    }

    private fun fixture(name: String): JsonObject {
        val path = contractFixturesDir().resolve(name)
        return json.parseToJsonElement(String(Files.readAllBytes(path))).jsonObject
    }

    private fun contractFixturesDir(): Path {
        val cwd = Paths.get(System.getProperty("user.dir"))
        return cwd.resolve("..").resolve("docs").resolve("contracts").resolve("fixtures").normalize()
    }

    private fun JsonObject.string(key: String): String = getValue(key).jsonPrimitive.content

    private fun JsonObject.int(key: String): Int = getValue(key).jsonPrimitive.content.toInt()
}
