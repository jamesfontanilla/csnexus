package com.csnexus.app.core.auth

import com.csnexus.app.core.logging.AppLogger
import com.csnexus.app.core.logging.DiagnosticsContext
import com.csnexus.app.core.logging.LogLevel
import com.csnexus.app.core.logging.NoOpAppLogger
import com.csnexus.app.core.logging.toDiagnosticsContext
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.core.network.safeApiCall
import com.csnexus.app.feature.auth.data.AuthApi
import com.csnexus.app.feature.auth.data.EmailVerificationRequestDto
import com.csnexus.app.feature.auth.data.DeleteAccountRequestDto
import com.csnexus.app.feature.auth.data.GoogleAuthRequestDto
import com.csnexus.app.feature.auth.data.LoginRequestDto
import com.csnexus.app.feature.auth.data.PasswordChangeRequestDto
import com.csnexus.app.feature.auth.data.PasswordResetDto
import com.csnexus.app.feature.auth.data.PasswordResetRequestDto
import com.csnexus.app.feature.auth.data.SignupRequestDto
import com.csnexus.app.feature.auth.data.UpdateUserRequestDto
import com.csnexus.app.feature.auth.data.UserDto

class AuthRepository(
    private val authApi: AuthApi,
    private val tokenStore: TokenStore,
    private val sessionManager: SessionManager? = null,
    private val logger: AppLogger = NoOpAppLogger,
) {
    fun isAuthenticated(): Boolean = tokenStore.isAuthenticated()

    suspend fun login(email: String, password: String): ApiResult<Unit> {
        return when (val result = safeApiCall { authApi.login(LoginRequestDto(email, password)) }) {
            is ApiResult.Success -> {
                tokenStore.saveTokens(result.value.accessToken, result.value.refreshToken)
                sessionManager?.markAuthenticated()
                logger.log(
                    level = LogLevel.Info,
                    event = "auth_login_success",
                    context = DiagnosticsContext(
                        endpoint = "v1/auth/sessions",
                        extras = mapOf("email" to email),
                    ),
                    message = "Login completed",
                )
                ApiResult.Success(Unit)
            }
            is ApiResult.Failure -> {
                logger.log(
                    level = LogLevel.Error,
                    event = "auth_login_failure",
                    context = result.error.toDiagnosticsContext(
                        endpoint = "v1/auth/sessions",
                        extras = mapOf("email" to email, "password" to password),
                    ),
                    message = result.error.debugMessage(),
                )
                result
            }
        }
    }

    suspend fun loginWithGoogle(
        idToken: String,
        androidPackage: String,
        category: String? = null,
    ): ApiResult<Unit> {
        return when (
            val result = safeApiCall {
                authApi.googleLogin(
                    GoogleAuthRequestDto(
                        idToken = idToken,
                        category = category,
                        androidPackage = androidPackage,
                    ),
                )
            }
        ) {
            is ApiResult.Success -> {
                tokenStore.saveTokens(result.value.accessToken, result.value.refreshToken)
                sessionManager?.markAuthenticated()
                logger.log(
                    level = LogLevel.Info,
                    event = "auth_google_login_success",
                    context = DiagnosticsContext(
                        endpoint = "v1/auth/google",
                        extras = mapOf(
                            "android_package" to androidPackage,
                            "category" to category.orEmpty(),
                        ),
                    ),
                    message = "Google login completed",
                )
                ApiResult.Success(Unit)
            }
            is ApiResult.Failure -> {
                logger.log(
                    level = LogLevel.Error,
                    event = "auth_google_login_failure",
                    context = result.error.toDiagnosticsContext(
                        endpoint = "v1/auth/google",
                        extras = mapOf(
                            "android_package" to androidPackage,
                            "category" to category.orEmpty(),
                        ),
                    ),
                    message = result.error.debugMessage(),
                )
                result
            }
        }
    }

    suspend fun signup(
        email: String,
        displayName: String,
        username: String,
        password: String,
        age: Int,
        category: String,
    ): ApiResult<Unit> = safeApiCall {
        authApi.signup(
            SignupRequestDto(
                email = email,
                displayName = displayName,
                username = username,
                password = password,
                age = age,
                category = category,
            ),
        )
    }

    suspend fun requestPasswordReset(email: String): ApiResult<Unit> =
        safeApiCall { authApi.requestPasswordReset(PasswordResetRequestDto(email)) }

    suspend fun verifyEmail(email: String, code: String): ApiResult<Unit> {
        return when (
            val result = safeApiCall {
                authApi.verifyEmail(EmailVerificationRequestDto(email = email, code = code))
            }
        ) {
            is ApiResult.Success -> {
                result.value.token?.let {
                    tokenStore.saveAccessToken(it)
                    sessionManager?.markAuthenticated()
                }
                ApiResult.Success(Unit)
            }
            is ApiResult.Failure -> result
        }
    }

    suspend fun resetPassword(email: String, code: String, newPassword: String): ApiResult<Unit> =
        safeApiCall {
            authApi.resetPassword(
                PasswordResetDto(
                    email = email,
                    code = code,
                    newPassword = newPassword,
                ),
            )
        }

    suspend fun currentUser(): ApiResult<UserDto> = safeApiCall { authApi.me() }

    suspend fun updateDisplayName(displayName: String): ApiResult<UserDto> =
        safeApiCall { authApi.updateMe(UpdateUserRequestDto(displayName = displayName)) }

    suspend fun updateProfile(displayName: String, timezone: String): ApiResult<UserDto> =
        safeApiCall {
            authApi.updateMe(
                UpdateUserRequestDto(
                    displayName = displayName,
                    timezone = timezone,
                ),
            )
        }

    suspend fun changePassword(currentPassword: String, newPassword: String): ApiResult<Unit> =
        safeApiCall {
            authApi.changePassword(
                PasswordChangeRequestDto(
                    currentPassword = currentPassword,
                    newPassword = newPassword,
                ),
            )
        }

    suspend fun deleteAccount(confirmationPhrase: String): ApiResult<Unit> {
        return when (
            val result = safeApiCall {
                authApi.deleteAccount(DeleteAccountRequestDto(confirmationPhrase))
            }
        ) {
            is ApiResult.Success -> {
                logger.log(
                    level = LogLevel.Info,
                    event = "auth_delete_account_success",
                    context = DiagnosticsContext(
                        endpoint = "v1/users/me",
                        extras = mapOf("confirmation_phrase" to confirmationPhrase),
                    ),
                    message = "Delete account completed",
                )
                clearLocalSession()
                ApiResult.Success(Unit)
            }
            is ApiResult.Failure -> {
                logger.log(
                    level = LogLevel.Error,
                    event = "auth_delete_account_failure",
                    context = result.error.toDiagnosticsContext(
                        endpoint = "v1/users/me",
                        extras = mapOf("confirmation_phrase" to confirmationPhrase),
                    ),
                    message = result.error.debugMessage(),
                )
                result
            }
        }
    }

    fun clearLocalSession() {
        sessionManager?.clearSession() ?: tokenStore.clear()
    }

    suspend fun logout() {
        runCatching { authApi.logout() }
        logger.info("auth_logout=started")
        clearLocalSession()
        logger.info("auth_logout=completed")
    }
}

private fun com.csnexus.app.core.error.AppError.debugMessage(): String = when (this) {
    is com.csnexus.app.core.error.AppError.Http -> message
    is com.csnexus.app.core.error.AppError.Network -> message
    is com.csnexus.app.core.error.AppError.Serialization -> message
    is com.csnexus.app.core.error.AppError.Unknown -> message
}
