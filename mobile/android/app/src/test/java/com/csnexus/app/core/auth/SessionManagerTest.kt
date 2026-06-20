package com.csnexus.app.core.auth

import com.csnexus.app.feature.auth.data.AuthApi
import com.csnexus.app.feature.auth.data.DeleteAccountRequestDto
import com.csnexus.app.feature.auth.data.EmailVerificationRequestDto
import com.csnexus.app.feature.auth.data.EmailVerificationResponseDto
import com.csnexus.app.feature.auth.data.GoogleAuthRequestDto
import com.csnexus.app.feature.auth.data.LoginRequestDto
import com.csnexus.app.feature.auth.data.LoginResponseDto
import com.csnexus.app.feature.auth.data.PasswordChangeRequestDto
import com.csnexus.app.feature.auth.data.PasswordResetDto
import com.csnexus.app.feature.auth.data.PasswordResetRequestDto
import com.csnexus.app.feature.auth.data.RefreshSessionRequestDto
import com.csnexus.app.feature.auth.data.SignupRequestDto
import com.csnexus.app.feature.auth.data.UpdateUserRequestDto
import com.csnexus.app.feature.auth.data.UserDto
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.delay
import kotlinx.coroutines.test.runTest
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.ResponseBody.Companion.toResponseBody
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import retrofit2.HttpException
import retrofit2.Response

class SessionManagerTest {
    @Test
    fun refreshAccessTokenUsesSingleFlightForConcurrentFailures() = runTest {
        val tokenStore = MemoryTokenStore().apply {
            saveTokens("old-access", "old-refresh")
        }
        val authApi = RefreshingAuthApi(
            response = LoginResponseDto(
                accessToken = "new-access",
                refreshToken = "new-refresh",
                expiresIn = 900,
            ),
            delayMillis = 20,
        )
        val sessionManager = SessionManager(tokenStoreProvider = { tokenStore }).apply {
            bindAuthApi(authApi)
        }

        val results = List(8) {
            async { sessionManager.refreshAccessToken(failedAccessToken = "old-access") }
        }.awaitAll()

        assertTrue(results.all { it })
        assertEquals(1, authApi.refreshCalls)
        assertEquals("new-access", tokenStore.accessToken())
        assertEquals("new-refresh", tokenStore.refreshToken())
        assertEquals(AuthState.Authenticated, sessionManager.authState.value)
    }

    @Test
    fun refreshKeepsCurrentRefreshTokenWhenBackendDoesNotRotate() = runTest {
        val tokenStore = MemoryTokenStore().apply {
            saveTokens("old-access", "stable-refresh")
        }
        val sessionManager = SessionManager(tokenStoreProvider = { tokenStore }).apply {
            bindAuthApi(
                RefreshingAuthApi(
                    response = LoginResponseDto(accessToken = "new-access", expiresIn = 900),
                ),
            )
        }

        assertTrue(sessionManager.refreshAccessToken(failedAccessToken = "old-access"))
        assertEquals("new-access", tokenStore.accessToken())
        assertEquals("stable-refresh", tokenStore.refreshToken())
    }

    @Test
    fun permanentRefreshFailureClearsSession() = runTest {
        val tokenStore = MemoryTokenStore().apply {
            saveTokens("old-access", "revoked-refresh")
        }
        val sessionManager = SessionManager(tokenStoreProvider = { tokenStore }).apply {
            bindAuthApi(RevokedRefreshAuthApi())
        }

        assertFalse(sessionManager.refreshAccessToken(failedAccessToken = "old-access"))
        assertEquals(null, tokenStore.accessToken())
        assertEquals(null, tokenStore.refreshToken())
        assertEquals(AuthState.Unauthenticated, sessionManager.authState.value)
    }

    @Test
    fun logoutClearsSessionManagerTokens() = runTest {
        val tokenStore = MemoryTokenStore().apply {
            saveTokens("access-token", "refresh-token")
        }
        val sessionManager = SessionManager(tokenStoreProvider = { tokenStore })
        val repository = AuthRepository(
            authApi = RefreshingAuthApi(
                response = LoginResponseDto(accessToken = "unused", expiresIn = 900),
            ),
            tokenStore = tokenStore,
            sessionManager = sessionManager,
        )

        repository.logout()

        assertEquals(null, tokenStore.accessToken())
        assertEquals(null, tokenStore.refreshToken())
        assertEquals(AuthState.Unauthenticated, sessionManager.authState.value)
    }
}

private class MemoryTokenStore : TokenStore {
    private var accessToken: String? = null
    private var refreshToken: String? = null

    override fun accessToken(): String? = accessToken

    override fun refreshToken(): String? = refreshToken

    override fun saveTokens(accessToken: String, refreshToken: String?) {
        this.accessToken = accessToken
        this.refreshToken = refreshToken
    }

    override fun clear() {
        accessToken = null
        refreshToken = null
    }
}

private open class RefreshingAuthApi(
    private val response: LoginResponseDto,
    private val delayMillis: Long = 0,
) : AuthApi {
    var refreshCalls: Int = 0
        private set

    override suspend fun login(request: LoginRequestDto): LoginResponseDto = response

    override suspend fun googleLogin(request: GoogleAuthRequestDto): LoginResponseDto = response

    override suspend fun refreshSession(request: RefreshSessionRequestDto): LoginResponseDto {
        refreshCalls++
        if (delayMillis > 0) delay(delayMillis)
        return response
    }

    override suspend fun signup(request: SignupRequestDto) = Unit

    override suspend fun requestPasswordReset(request: PasswordResetRequestDto) = Unit

    override suspend fun verifyEmail(request: EmailVerificationRequestDto): EmailVerificationResponseDto =
        EmailVerificationResponseDto()

    override suspend fun resetPassword(request: PasswordResetDto) = Unit

    override suspend fun me(): UserDto = UserDto(
        id = 1,
        email = "learner@example.com",
        displayName = "Learner",
        username = "learner",
        category = "PROFESSIONAL",
    )

    override suspend fun updateMe(request: UpdateUserRequestDto): UserDto = me().copy(
        displayName = request.displayName ?: "Learner",
        username = request.username ?: "learner",
        timezone = request.timezone,
    )

    override suspend fun changePassword(request: PasswordChangeRequestDto) = Unit

    override suspend fun deleteAccount(request: DeleteAccountRequestDto) = Unit

    override suspend fun logout() = Unit
}

private class RevokedRefreshAuthApi : RefreshingAuthApi(
    response = LoginResponseDto(accessToken = "unused", expiresIn = 900),
) {
    override suspend fun refreshSession(request: RefreshSessionRequestDto): LoginResponseDto {
        throw HttpException(
            Response.error<Unit>(
                401,
                """{"error":{"code":"REFRESH_TOKEN_REVOKED","message":"Refresh token revoked."}}"""
                    .toResponseBody("application/json".toMediaType()),
            ),
        )
    }
}
