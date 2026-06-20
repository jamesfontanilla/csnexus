package com.csnexus.app.core.network

import com.csnexus.app.core.logging.AppLogger
import okhttp3.Interceptor
import okhttp3.Response

class DiagnosticsInterceptor(
    private val logger: AppLogger,
) : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        val request = chain.request()
        val endpoint = request.url.encodedPath
        val method = request.method

        logger.networkEvent(
            event = "network_request",
            endpoint = endpoint,
            method = method,
            message = "Request started",
        )

        return try {
            val response = chain.proceed(request)
            logger.networkEvent(
                event = "network_response",
                endpoint = endpoint,
                method = method,
                requestId = response.header("X-Request-ID"),
                statusCode = response.code,
                message = "Request completed",
            )
            response
        } catch (throwable: Throwable) {
            logger.networkEvent(
                event = "network_failure",
                endpoint = endpoint,
                method = method,
                message = throwable.message ?: "Request failed before response",
                throwable = throwable,
            )
            throw throwable
        }
    }
}
