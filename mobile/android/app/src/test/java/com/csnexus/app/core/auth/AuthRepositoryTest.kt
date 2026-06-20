package com.csnexus.app.core.auth

import com.csnexus.app.core.network.ApiResult
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
import kotlinx.coroutines.test.runTest
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class AuthRepositoryTest {
    @Test
    fun loginStoresAccessAndRefreshTokens() = runTest {
        val tokenStore = InMemoryTokenStore()
        val repository = AuthRepository(
            authApi = FakeAuthApi(
                loginResponse = LoginResponseDto(
                    accessToken = "access-token",
                    refreshToken = "refresh-token",
                    expiresIn = 900,
                    refreshExpiresIn = 2_592_000,
                ),
            ),
            tokenStore = tokenStore,
        )

        val result = repository.login("learner@example.com", "Password1!")

        assertTrue(result is ApiResult.Success)
        assertEquals("access-token", tokenStore.accessToken())
        assertEquals("refresh-token", tokenStore.refreshToken())
        assertTrue(tokenStore.isAuthenticated())
    }

    @Test
    fun loginClearsStaleRefreshTokenWhenBackendOmitsIt() = runTest {
        val tokenStore = InMemoryTokenStore().apply {
            saveTokens("old-access", "old-refresh")
        }
        val repository = AuthRepository(
            authApi = FakeAuthApi(
                loginResponse = LoginResponseDto(
                    accessToken = "access-token",
                    expiresIn = 900,
                ),
            ),
            tokenStore = tokenStore,
        )

        repository.login("learner@example.com", "Password1!")

        assertEquals("access-token", tokenStore.accessToken())
        assertEquals(null, tokenStore.refreshToken())
    }

    @Test
    fun googleLoginStoresTokensAndSendsAndroidPackage() = runTest {
        val tokenStore = InMemoryTokenStore()
        val repository = AuthRepository(
            authApi = FakeAuthApi(
                loginResponse = LoginResponseDto(
                    accessToken = "google-access-token",
                    refreshToken = "google-refresh-token",
                    expiresIn = 900,
                    refreshExpiresIn = 2_592_000,
                ),
            ),
            tokenStore = tokenStore,
        )

        val result = repository.loginWithGoogle(
            idToken = "google-id-token",
            androidPackage = "com.csnexus.app",
        )

        assertTrue(result is ApiResult.Success)
        assertEquals("google-access-token", tokenStore.accessToken())
        assertEquals("google-refresh-token", tokenStore.refreshToken())
    }
}

private class InMemoryTokenStore : TokenStore {
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

private class FakeAuthApi(
    private val loginResponse: LoginResponseDto,
) : AuthApi {
    override suspend fun login(request: LoginRequestDto): LoginResponseDto = loginResponse

    override suspend fun googleLogin(request: GoogleAuthRequestDto): LoginResponseDto = loginResponse

    override suspend fun refreshSession(request: RefreshSessionRequestDto): LoginResponseDto = loginResponse

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
