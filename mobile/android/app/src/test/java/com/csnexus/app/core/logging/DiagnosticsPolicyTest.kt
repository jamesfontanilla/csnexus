package com.csnexus.app.core.logging

import com.csnexus.app.core.error.AppError
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class DiagnosticsPolicyTest {
    @Test
    fun authFailureDiagnosticsRedactSecretsAndProfileData() {
        val rendered = render(
            event = "auth_login_failure",
            error = AppError.Http(
                statusCode = 401,
                code = "INVALID_CREDENTIALS",
                message = "Login failed",
                requestId = "req-auth-1",
            ),
            endpoint = "v1/auth/sessions",
            screenName = "Login",
            extras = mapOf(
                "email" to "learner@example.com",
                "password" to "Password1!",
                "otp_code" to "123456",
            ),
        )

        assertTrue(rendered.contains("request_id=req-auth-1"))
        assertTrue(rendered.contains("status_class=4xx"))
        assertTrue(rendered.contains("error_code=INVALID_CREDENTIALS"))
        assertTrue(rendered.contains("email=<redacted>"))
        assertTrue(rendered.contains("password=<redacted>"))
        assertTrue(rendered.contains("otp_code=<redacted>"))
        assertFalse(rendered.contains("learner@example.com"))
        assertFalse(rendered.contains("Password1!"))
        assertFalse(rendered.contains("123456"))
    }

    @Test
    fun lessonFailureDiagnosticsRedactLessonAnswers() {
        val rendered = render(
            event = "lesson_completion_failure",
            error = AppError.Http(
                statusCode = 409,
                code = "LESSON_STALE",
                message = "Lesson stale",
                requestId = "req-lesson-1",
            ),
            endpoint = "v1/subtopics/77/lesson:complete",
            screenName = "Lesson",
            extras = mapOf("answer" to "The singular verb."),
        )

        assertTrue(rendered.contains("error_code=LESSON_STALE"))
        assertTrue(rendered.contains("answer=<redacted>"))
        assertFalse(rendered.contains("The singular verb."))
    }

    @Test
    fun quizFailureDiagnosticsRedactSelectedAnswers() {
        val rendered = render(
            event = "quiz_answer_failure",
            error = AppError.Http(
                statusCode = 422,
                code = "INVALID_ANSWER",
                message = "Answer rejected",
                requestId = "req-quiz-1",
            ),
            endpoint = "v1/quiz-attempts/5/answers/8",
            screenName = "Quiz",
            extras = mapOf("selected_answer" to "B"),
        )

        assertTrue(rendered.contains("selected_answer=<redacted>"))
        assertFalse(rendered.contains("selected_answer=B"))
    }

    @Test
    fun adminFailureDiagnosticsRedactAdminSensitiveValues() {
        val rendered = render(
            event = "admin_delete_failure",
            error = AppError.Http(
                statusCode = 403,
                code = "FORBIDDEN",
                message = "Cannot delete user",
                requestId = "req-admin-1",
            ),
            endpoint = "v1/admin/users/4",
            screenName = "Admin",
            extras = mapOf(
                "admin_email" to "admin@example.com",
                "target_email" to "learner@example.com",
            ),
        )

        assertTrue(rendered.contains("admin_email=<redacted>"))
        assertTrue(rendered.contains("target_email=<redacted>"))
        assertFalse(rendered.contains("admin@example.com"))
        assertFalse(rendered.contains("learner@example.com"))
    }

    @Test
    fun tutorFailureDiagnosticsRedactTutorMessages() {
        val rendered = render(
            event = "tutor_failure",
            error = AppError.Http(
                statusCode = 500,
                code = "TUTOR_UNAVAILABLE",
                message = "Tutor unavailable",
                requestId = "req-tutor-1",
            ),
            endpoint = "v1/tutor/lesson-chat",
            screenName = "Tutor",
            extras = mapOf(
                "tutor_message" to "Explain why the answer is B",
                "history" to "Question and reply transcript",
            ),
        )

        assertTrue(rendered.contains("tutor_message=<redacted>"))
        assertTrue(rendered.contains("history=<redacted>"))
        assertFalse(rendered.contains("Explain why the answer is B"))
        assertFalse(rendered.contains("Question and reply transcript"))
    }

    @Test
    fun syncFailureDiagnosticsKeepSyncEventIdAndErrorCode() {
        val rendered = formatDiagnosticLog(
            event = "sync_failure",
            context = AppError.Http(
                statusCode = 401,
                code = "AUTH_EXPIRED",
                message = "Sync auth expired",
                requestId = "req-sync-1",
            ).toDiagnosticsContext(
                endpoint = "v1/goals/me/target",
                syncEventId = "goal_target_update:abc123",
            ),
            message = "Sync failed",
        )

        assertTrue(rendered.contains("sync_event_id=goal_target_update:abc123"))
        assertTrue(rendered.contains("request_id=req-sync-1"))
        assertTrue(rendered.contains("status_class=4xx"))
        assertTrue(rendered.contains("error_code=AUTH_EXPIRED"))
    }

    private fun render(
        event: String,
        error: AppError,
        endpoint: String,
        screenName: String,
        extras: Map<String, String>,
    ): String {
        return formatDiagnosticLog(
            event = event,
            context = error.toDiagnosticsContext(
                endpoint = endpoint,
                screenName = screenName,
                extras = extras,
            ),
            message = when (error) {
                is AppError.Http -> error.message
                is AppError.Network -> error.message
                is AppError.Serialization -> error.message
                is AppError.Unknown -> error.message
            },
        )
    }
}
