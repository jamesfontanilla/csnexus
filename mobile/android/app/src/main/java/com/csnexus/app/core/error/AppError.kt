package com.csnexus.app.core.error

sealed interface AppError {
    data class Http(
        val statusCode: Int,
        val code: String,
        val message: String,
        val requestId: String?,
    ) : AppError

    data class Network(val message: String) : AppError
    data class Serialization(val message: String) : AppError
    data class Unknown(val message: String) : AppError
}

fun AppError.userMessage(): String = when (this) {
    is AppError.Http -> message.ifBlank { "Request failed." }
    is AppError.Network -> "You appear to be offline. Check your connection and try again."
    is AppError.Serialization -> "The server response could not be read."
    is AppError.Unknown -> "Something went wrong. Please try again."
}
