package com.csnexus.app.feature.auth.data

import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.HTTP
import retrofit2.http.PATCH
import retrofit2.http.POST

interface AuthApi {
    @POST("v1/auth/sessions")
    suspend fun login(@Body request: LoginRequestDto): LoginResponseDto

    @POST("v1/auth/google")
    suspend fun googleLogin(@Body request: GoogleAuthRequestDto): LoginResponseDto

    @POST("v1/auth/sessions:refresh")
    suspend fun refreshSession(@Body request: RefreshSessionRequestDto): LoginResponseDto

    @POST("v1/auth/signups")
    suspend fun signup(@Body request: SignupRequestDto)

    @POST("v1/auth/password-reset-requests")
    suspend fun requestPasswordReset(@Body request: PasswordResetRequestDto)

    @POST("v1/auth/email-verifications")
    suspend fun verifyEmail(@Body request: EmailVerificationRequestDto): EmailVerificationResponseDto

    @POST("v1/auth/password-resets")
    suspend fun resetPassword(@Body request: PasswordResetDto)

    @GET("v1/auth/me")
    suspend fun me(): UserDto

    @PATCH("v1/users/me")
    suspend fun updateMe(@Body request: UpdateUserRequestDto): UserDto

    @POST("v1/auth/password-change")
    suspend fun changePassword(@Body request: PasswordChangeRequestDto)

    @HTTP(method = "DELETE", path = "v1/users/me", hasBody = true)
    suspend fun deleteAccount(@Body request: DeleteAccountRequestDto)

    @DELETE("v1/auth/sessions/me")
    suspend fun logout()
}
