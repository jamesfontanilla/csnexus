package com.csnexus.app.feature.admin.data

import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.core.network.safeApiCall

/**
 * Contract for admin data access. Extracting an interface keeps the ViewModel
 * testable without a mocking framework.
 */
interface AdminRepositoryContract {
    suspend fun analytics(): ApiResult<AdminAnalyticsDto>
    suspend fun users(search: String? = null): ApiResult<AdminUsersResponseDto>
    suspend fun banUser(userId: Int): ApiResult<AdminUserDto>
    suspend fun unbanUser(userId: Int): ApiResult<AdminUserDto>
    suspend fun deleteUser(userId: Int): ApiResult<Unit>
}

open class AdminRepository(
    private val adminApi: AdminApi,
) : AdminRepositoryContract {

    override suspend fun analytics(): ApiResult<AdminAnalyticsDto> =
        safeApiCall { adminApi.analytics() }

    override suspend fun users(search: String?): ApiResult<AdminUsersResponseDto> =
        safeApiCall { adminApi.users(search = search) }

    override suspend fun banUser(userId: Int): ApiResult<AdminUserDto> =
        safeApiCall { adminApi.updateUser(userId, AdminUpdateUserRequestDto(isBanned = true)) }

    override suspend fun unbanUser(userId: Int): ApiResult<AdminUserDto> =
        safeApiCall { adminApi.updateUser(userId, AdminUpdateUserRequestDto(isBanned = false)) }

    override suspend fun deleteUser(userId: Int): ApiResult<Unit> =
        safeApiCall { adminApi.deleteUser(userId) }
}
