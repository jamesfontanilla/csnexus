package com.csnexus.app.core.network

import com.csnexus.app.core.error.AppError
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import retrofit2.HttpException
import java.io.IOException

sealed interface ApiResult<out T> {
    data class Success<T>(val value: T) : ApiResult<T>
    data class Failure(val error: AppError) : ApiResult<Nothing>
}

suspend fun <T> safeApiCall(call: suspend () -> T): ApiResult<T> {
    return try {
        ApiResult.Success(call())
    } catch (error: HttpException) {
        ApiResult.Failure(ApiErrorMapper.fromHttpException(error))
    } catch (error: IOException) {
        ApiResult.Failure(AppError.Network(error.message ?: "Network unavailable"))
    } catch (error: RuntimeException) {
        ApiResult.Failure(AppError.Unknown(error.message ?: "Unknown error"))
    }
}

@Serializable
data class BackendErrorEnvelope(
    val error: BackendError? = null,
    val detail: String? = null,
)

@Serializable
data class BackendError(
    val message: String? = null,
    val code: String? = null,
)

object ApiErrorMapper {
    private val json = Json { ignoreUnknownKeys = true }

    fun fromHttpException(error: HttpException): AppError {
        val requestId = error.response()?.headers()?.get("X-Request-ID")
        val rawBody = error.response()?.errorBody()?.string()
        val envelope = rawBody?.let(::decodeErrorEnvelope)
        val message = envelope?.error?.message
            ?: envelope?.detail
            ?: "Request failed with status ${error.code()}"
        val code = envelope?.error?.code ?: "HTTP_${error.code()}"
        return AppError.Http(
            statusCode = error.code(),
            code = code,
            message = message,
            requestId = requestId,
        )
    }

    fun decodeErrorEnvelope(rawBody: String): BackendErrorEnvelope? {
        return runCatching { json.decodeFromString<BackendErrorEnvelope>(rawBody) }.getOrNull()
    }
}
