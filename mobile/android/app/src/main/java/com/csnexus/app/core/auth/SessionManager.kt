package com.csnexus.app.core.auth

import com.csnexus.app.core.error.AppError
import com.csnexus.app.core.logging.AppLogger
import com.csnexus.app.core.logging.NoOpAppLogger
import com.csnexus.app.core.logging.toDiagnosticsContext
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.core.network.safeApiCall
import com.csnexus.app.feature.auth.data.AuthApi
import com.csnexus.app.feature.auth.data.RefreshSessionRequestDto
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext

sealed interface AuthState {
    data object Authenticated : AuthState
    data object Refreshing : AuthState
    data object Unauthenticated : AuthState
}

class SessionManager(
    private val tokenStoreProvider: () -> TokenStore,
    private val logger: AppLogger = NoOpAppLogger,
) {
    private val tokenStore: TokenStore by lazy(tokenStoreProvider)
    private val refreshMutex = Mutex()
    private var authApi: AuthApi? = null
    private val _authState = MutableStateFlow<AuthState>(AuthState.Unauthenticated)
    val authState: StateFlow<AuthState> = _authState.asStateFlow()

    fun bindAuthApi(authApi: AuthApi) {
        this.authApi = authApi
    }

    fun accessToken(): String? = tokenStore.accessToken()

    suspend fun initializeFromStore() {
        val nextState = withContext(Dispatchers.IO) {
            if (tokenStore.isAuthenticated()) AuthState.Authenticated else AuthState.Unauthenticated
        }
        _authState.value = nextState
    }

    fun markAuthenticated() {
        _authState.value = AuthState.Authenticated
        logger.info("auth_state=authenticated")
    }

    fun clearSession() {
        tokenStore.clear()
        _authState.value = AuthState.Unauthenticated
        logger.info("auth_state=unauthenticated")
    }

    suspend fun refreshAccessToken(failedAccessToken: String? = null): Boolean {
        val refreshToken = tokenStore.refreshToken()
        if (refreshToken.isNullOrBlank()) {
            logger.error("auth_refresh=skipped reason=no_refresh_token")
            clearSession()
            return false
        }

        return refreshMutex.withLock {
            if (failedAccessToken != null && tokenStore.accessToken() != failedAccessToken) {
                _authState.value = AuthState.Authenticated
                return@withLock true
            }

            val latestRefreshToken = tokenStore.refreshToken()
            val api = authApi
            if (latestRefreshToken.isNullOrBlank() || api == null) {
                clearSession()
                return@withLock false
            }

            _authState.value = AuthState.Refreshing
            logger.info("auth_refresh=started")
            when (
                val result = safeApiCall {
                    api.refreshSession(RefreshSessionRequestDto(latestRefreshToken))
                }
            ) {
                is ApiResult.Success -> {
                    val nextRefreshToken = result.value.refreshToken ?: latestRefreshToken
                    tokenStore.saveTokens(result.value.accessToken, nextRefreshToken)
                    _authState.value = AuthState.Authenticated
                    logger.info("auth_refresh=success")
                    true
                }
                is ApiResult.Failure -> {
                    logger.log(
                        level = com.csnexus.app.core.logging.LogLevel.Error,
                        event = "auth_refresh_failure",
                        context = result.error.toDiagnosticsContext(endpoint = "v1/auth/sessions:refresh"),
                        message = result.error.userSafeDebugMessage(),
                    )
                    if (result.error.isPermanentRefreshFailure()) {
                        clearSession()
                    } else {
                        _authState.value = AuthState.Authenticated
                    }
                    false
                }
            }
        }
    }
}

private fun AppError.isPermanentRefreshFailure(): Boolean {
    return this is AppError.Http && statusCode in setOf(400, 401, 403)
}

private fun AppError.userSafeDebugMessage(): String = when (this) {
    is AppError.Http -> message
    is AppError.Network -> this.message
    is AppError.Serialization -> this.message
    is AppError.Unknown -> this.message
}
