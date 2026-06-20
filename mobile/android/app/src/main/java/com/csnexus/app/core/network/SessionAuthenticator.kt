package com.csnexus.app.core.network

import com.csnexus.app.core.auth.SessionManager
import kotlinx.coroutines.runBlocking
import okhttp3.Authenticator
import okhttp3.Request
import okhttp3.Response
import okhttp3.Route

class SessionAuthenticator(
    private val sessionManager: SessionManager,
) : Authenticator {
    override fun authenticate(route: Route?, response: Response): Request? {
        if (response.request.isRefreshRequest() || response.responseCount() >= MAX_AUTH_ATTEMPTS) {
            return null
        }

        val failedAccessToken = response.request.header("Authorization")?.removePrefix("Bearer ")
        val refreshed = runBlocking {
            sessionManager.refreshAccessToken(failedAccessToken)
        }
        if (!refreshed) return null

        val nextAccessToken = sessionManager.accessToken()
        if (nextAccessToken.isNullOrBlank()) return null

        return response.request.newBuilder()
            .header("Authorization", "Bearer $nextAccessToken")
            .build()
    }

    private companion object {
        const val MAX_AUTH_ATTEMPTS = 2
    }
}

internal fun Request.isRefreshRequest(): Boolean {
    return url.toString().contains("/v1/auth/sessions:refresh")
}

private fun Response.responseCount(): Int {
    var count = 1
    var priorResponse = priorResponse
    while (priorResponse != null) {
        count++
        priorResponse = priorResponse.priorResponse
    }
    return count
}
