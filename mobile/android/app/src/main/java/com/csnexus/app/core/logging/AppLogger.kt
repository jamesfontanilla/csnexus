package com.csnexus.app.core.logging

import android.util.Log
import com.csnexus.app.core.error.AppError

enum class LogLevel {
    Info,
    Error,
}

data class DiagnosticsContext(
    val screenName: String? = null,
    val route: String? = null,
    val endpoint: String? = null,
    val requestId: String? = null,
    val statusClass: String? = null,
    val syncEventId: String? = null,
    val extras: Map<String, String> = emptyMap(),
)

interface AppLogger {
    fun log(
        level: LogLevel,
        event: String,
        context: DiagnosticsContext = DiagnosticsContext(),
        message: String? = null,
        throwable: Throwable? = null,
    )

    fun info(message: String) {
        log(level = LogLevel.Info, event = "message", message = message)
    }

    fun error(message: String, throwable: Throwable? = null) {
        log(level = LogLevel.Error, event = "message", message = message, throwable = throwable)
    }

    fun screenView(screenName: String, route: String) {
        log(
            level = LogLevel.Info,
            event = "screen_view",
            context = DiagnosticsContext(screenName = screenName, route = route),
            message = "Screen opened",
        )
    }

    fun networkEvent(
        event: String,
        endpoint: String,
        method: String,
        requestId: String? = null,
        statusCode: Int? = null,
        message: String? = null,
        throwable: Throwable? = null,
    ) {
        log(
            level = if (throwable == null && statusCode?.let { it < 400 } != false) LogLevel.Info else LogLevel.Error,
            event = event,
            context = DiagnosticsContext(
                endpoint = endpoint,
                requestId = requestId,
                statusClass = statusCode?.toStatusClass(),
                extras = buildMap {
                    put("method", method)
                    statusCode?.let { put("status_code", it.toString()) }
                },
            ),
            message = message,
            throwable = throwable,
        )
    }

    fun syncEvent(
        event: String,
        syncEventId: String,
        endpoint: String,
        statusCode: Int? = null,
        requestId: String? = null,
        message: String? = null,
        errorCode: String? = null,
    ) {
        log(
            level = if (statusCode?.let { it >= 400 } == true) LogLevel.Error else LogLevel.Info,
            event = event,
            context = DiagnosticsContext(
                endpoint = endpoint,
                requestId = requestId,
                statusClass = statusCode?.toStatusClass(),
                syncEventId = syncEventId,
                extras = buildMap {
                    errorCode?.let { put("error_code", it) }
                },
            ),
            message = message,
        )
    }
}

class AndroidAppLogger(
    private val tag: String = "CSNexus",
) : AppLogger {
    override fun log(
        level: LogLevel,
        event: String,
        context: DiagnosticsContext,
        message: String?,
        throwable: Throwable?,
    ) {
        val rendered = formatDiagnosticLog(event = event, context = context, message = message)
        when (level) {
            LogLevel.Info -> Log.i(tag, rendered)
            LogLevel.Error -> Log.e(tag, rendered, throwable)
        }
    }
}

object NoOpAppLogger : AppLogger {
    override fun log(
        level: LogLevel,
        event: String,
        context: DiagnosticsContext,
        message: String?,
        throwable: Throwable?,
    ) = Unit
}

fun formatDiagnosticLog(
    event: String,
    context: DiagnosticsContext = DiagnosticsContext(),
    message: String? = null,
): String {
    val parts = mutableListOf("event=$event")
    context.screenName?.let { parts += "screen=${redactSensitive(it)}" }
    context.route?.let { parts += "route=${redactSensitive(it)}" }
    context.endpoint?.let { parts += "endpoint=${redactSensitive(it)}" }
    context.requestId?.let { parts += "request_id=${redactSensitive(it)}" }
    context.statusClass?.let { parts += "status_class=$it" }
    context.syncEventId?.let { parts += "sync_event_id=${redactSensitive(it)}" }
    sanitizeDiagnosticExtras(context.extras).forEach { (key, value) ->
        parts += "$key=$value"
    }
    message?.takeIf { it.isNotBlank() }?.let { parts += "message=${redactSensitive(it)}" }
    return parts.joinToString(" ")
}

fun sanitizeDiagnosticExtras(extras: Map<String, String>): Map<String, String> {
    return extras.mapValues { (key, value) ->
        if (key.isSensitiveDiagnosticKey()) {
            "<redacted>"
        } else {
            redactSensitive(value)
        }
    }
}

fun AppError.toDiagnosticsContext(
    endpoint: String? = null,
    screenName: String? = null,
    syncEventId: String? = null,
    extras: Map<String, String> = emptyMap(),
): DiagnosticsContext {
    val requestId = (this as? AppError.Http)?.requestId
    val statusCode = (this as? AppError.Http)?.statusCode
    val errorCode = (this as? AppError.Http)?.code
    return DiagnosticsContext(
        screenName = screenName,
        endpoint = endpoint,
        requestId = requestId,
        statusClass = statusCode?.toStatusClass(),
        syncEventId = syncEventId,
        extras = buildMap {
            putAll(extras)
            errorCode?.let { put("error_code", it) }
        },
    )
}

fun Int.toStatusClass(): String = "${this / 100}xx"

private fun String.isSensitiveDiagnosticKey(): Boolean {
    val normalized = lowercase()
    return normalized in sensitiveDiagnosticKeys ||
        normalized.endsWith("_token") ||
        normalized.endsWith("_password") ||
        (normalized.endsWith("_code") &&
            normalized != "error_code" &&
            normalized != "status_code") ||
        normalized.contains("authorization")
}

private val keyValueSensitiveRegex =
    Regex("(?i)(?<![A-Za-z0-9_])(access_token|refresh_token|password|current_password|new_password|otp|otp_code|verification_code|authorization|email|display_name|username|confirmation_phrase|selected_answer|correct_answer|answer|tutor_message|tutor_response|history|admin_email|target_email|code)=[^\\s&]+")

private val jsonSensitiveRegex =
    Regex("(?i)(\"(?:access_token|refresh_token|password|current_password|new_password|otp|otp_code|verification_code|authorization|email|display_name|username|confirmation_phrase|selected_answer|correct_answer|answer|tutor_message|tutor_response|history|admin_email|target_email|code)\"\\s*:\\s*\")([^\"]+)(\")")

private val bearerSensitiveRegex = Regex("(?i)(Authorization:\\s*Bearer\\s+)([^\\s]+)")

private val sensitiveDiagnosticKeys = setOf(
    "access_token",
    "refresh_token",
    "password",
    "current_password",
    "new_password",
    "otp",
    "otp_code",
    "verification_code",
    "authorization",
    "email",
    "display_name",
    "username",
    "confirmation_phrase",
    "selected_answer",
    "correct_answer",
    "answer",
    "tutor_message",
    "tutor_response",
    "history",
    "admin_email",
    "target_email",
    "code",
)

internal fun redactSensitive(message: String): String {
    return message
        .replace(keyValueSensitiveRegex) {
            "${it.groupValues[1]}=<redacted>"
        }
        .replace(jsonSensitiveRegex) {
            "${it.groupValues[1]}<redacted>${it.groupValues[3]}"
        }
        .replace(bearerSensitiveRegex) {
            "${it.groupValues[1]}<redacted>"
        }
}
