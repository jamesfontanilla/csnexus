package com.csnexus.app.feature.auth.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class LoginRequestDto(
    val email: String,
    val password: String,
)

@Serializable
data class LoginResponseDto(
    @SerialName("access_token")
    val accessToken: String,
    @SerialName("refresh_token")
    val refreshToken: String? = null,
    @SerialName("token_type")
    val tokenType: String = "Bearer",
    @SerialName("expires_in")
    val expiresIn: Int,
    @SerialName("refresh_expires_in")
    val refreshExpiresIn: Int? = null,
)

@Serializable
data class RefreshSessionRequestDto(
    @SerialName("refresh_token")
    val refreshToken: String,
)

@Serializable
data class GoogleAuthRequestDto(
    @SerialName("id_token")
    val idToken: String,
    val category: String? = null,
    val platform: String = "android",
    @SerialName("android_package")
    val androidPackage: String,
)

@Serializable
data class SignupRequestDto(
    val email: String,
    @SerialName("display_name")
    val displayName: String,
    val username: String,
    val password: String,
    val age: Int,
    val category: String,
)

@Serializable
data class PasswordResetRequestDto(
    val email: String,
)

@Serializable
data class EmailVerificationRequestDto(
    val email: String,
    val code: String,
    val purpose: String = "VERIFY_EMAIL",
)

@Serializable
data class PasswordResetDto(
    val email: String,
    val code: String,
    @SerialName("new_password")
    val newPassword: String,
)

@Serializable
data class EmailVerificationResponseDto(
    val token: String? = null,
)

@Serializable
data class UserDto(
    val id: Int,
    val email: String,
    @SerialName("display_name")
    val displayName: String,
    val username: String? = null,
    @SerialName("tz_name")
    val timezone: String? = null,
    val category: String,
    val role: String? = null,
)

@Serializable
data class UpdateUserRequestDto(
    @SerialName("display_name")
    val displayName: String? = null,
    val username: String? = null,
    @SerialName("tz_name")
    val timezone: String? = null,
)

@Serializable
data class PasswordChangeRequestDto(
    @SerialName("current_password")
    val currentPassword: String,
    @SerialName("new_password")
    val newPassword: String,
)

@Serializable
data class DeleteAccountRequestDto(
    @SerialName("confirmation_phrase")
    val confirmationPhrase: String,
)
