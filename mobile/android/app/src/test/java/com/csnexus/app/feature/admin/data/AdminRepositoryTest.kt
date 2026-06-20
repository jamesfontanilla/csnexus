package com.csnexus.app.feature.admin.data

import com.csnexus.app.core.error.AppError
import com.csnexus.app.core.network.ApiResult
import kotlinx.coroutines.test.runTest
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.ResponseBody.Companion.toResponseBody
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import retrofit2.HttpException
import retrofit2.Response
import java.io.IOException

class AdminRepositoryTest {

    // ── analytics ─────────────────────────────────────────────────────────────

    @Test
    fun analyticsSuccessReturnsDto() = runTest {
        val expected = makeAnalyticsDto(totalUsers = 100, verifiedUsers = 80, bannedUsers = 5)
        val repo = AdminRepository(FakeAdminApi(analyticsResponse = expected))

        val result = repo.analytics()

        assertTrue(result is ApiResult.Success)
        val dto = (result as ApiResult.Success).value
        assertEquals(100, dto.totalUsers)
        assertEquals(80, dto.verifiedUsers)
        assertEquals(5, dto.bannedUsers)
    }

    @Test
    fun analyticsHttpFailureMapsToApiResultFailure() = runTest {
        val repo = AdminRepository(FailingAdminApi(statusCode = 403))

        val result = repo.analytics()

        assertTrue(result is ApiResult.Failure)
        val err = (result as ApiResult.Failure).error
        assertTrue(err is AppError.Http)
        assertEquals(403, (err as AppError.Http).statusCode)
    }

    // ── users ─────────────────────────────────────────────────────────────────

    @Test
    fun usersSuccessReturnsList() = runTest {
        val users = listOf(makeUserDto(id = 1, email = "a@example.com"), makeUserDto(id = 2, email = "b@example.com"))
        val repo = AdminRepository(FakeAdminApi(usersResponse = AdminUsersResponseDto(items = users, total = 2)))

        val result = repo.users()

        assertTrue(result is ApiResult.Success)
        val dto = (result as ApiResult.Success).value
        assertEquals(2, dto.items.size)
        assertEquals(2, dto.total)
    }

    @Test
    fun usersNetworkFailureMapsToNetworkError() = runTest {
        val repo = AdminRepository(NetworkErrorAdminApi())

        val result = repo.users()

        assertTrue(result is ApiResult.Failure)
        assertTrue((result as ApiResult.Failure).error is AppError.Network)
    }

    // ── banUser ───────────────────────────────────────────────────────────────

    @Test
    fun banUserCallsUpdateWithIsBannedTrue() = runTest {
        val api = FakeAdminApi(updateUserResponse = makeUserDto(id = 7, isBanned = true))
        val repo = AdminRepository(api)

        val result = repo.banUser(7)

        assertTrue(result is ApiResult.Success)
        assertEquals(true, api.lastUpdateRequest?.isBanned)
        assertEquals(7, api.lastUpdateUserId)
        assertTrue((result as ApiResult.Success).value.isBanned)
    }

    // ── unbanUser ─────────────────────────────────────────────────────────────

    @Test
    fun unbanUserCallsUpdateWithIsBannedFalse() = runTest {
        val api = FakeAdminApi(updateUserResponse = makeUserDto(id = 3, isBanned = false))
        val repo = AdminRepository(api)

        val result = repo.unbanUser(3)

        assertTrue(result is ApiResult.Success)
        assertEquals(false, api.lastUpdateRequest?.isBanned)
    }

    // ── deleteUser ────────────────────────────────────────────────────────────

    @Test
    fun deleteUserSuccessReturnsSuccess() = runTest {
        val api = FakeAdminApi()
        val repo = AdminRepository(api)

        val result = repo.deleteUser(10)

        assertTrue(result is ApiResult.Success)
        assertEquals(10, api.lastDeleteUserId)
    }

    @Test
    fun deleteUserHttpFailureReturnsFailure() = runTest {
        val repo = AdminRepository(FailingAdminApi(statusCode = 404))

        val result = repo.deleteUser(99)

        assertTrue(result is ApiResult.Failure)
        assertTrue((result as ApiResult.Failure).error is AppError.Http)
    }
}

// ── Helpers ───────────────────────────────────────────────────────────────────

private fun makeAnalyticsDto(
    totalUsers: Int = 0,
    verifiedUsers: Int = 0,
    bannedUsers: Int = 0,
) = AdminAnalyticsDto(
    totalUsers = totalUsers,
    verifiedUsers = verifiedUsers,
    bannedUsers = bannedUsers,
    totalLessonsCompleted = 0,
    totalQuizAttempts = 0,
    totalMockAttempts = 0,
    mockPassRate = 0.0,
    weakestSubtopics = emptyList(),
)

private fun makeUserDto(
    id: Int = 1,
    email: String = "user@example.com",
    isBanned: Boolean = false,
) = AdminUserDto(
    id = id,
    email = email,
    displayName = "User $id",
    username = "user$id",
    role = "user",
    isBanned = isBanned,
)

// ── Fakes ─────────────────────────────────────────────────────────────────────

private class FakeAdminApi(
    private val analyticsResponse: AdminAnalyticsDto = makeAnalyticsDto(),
    private val usersResponse: AdminUsersResponseDto = AdminUsersResponseDto(items = emptyList(), total = 0),
    private val updateUserResponse: AdminUserDto = makeUserDto(),
) : AdminApi {

    var lastUpdateUserId: Int = -1
        private set
    var lastUpdateRequest: AdminUpdateUserRequestDto? = null
        private set
    var lastDeleteUserId: Int = -1
        private set

    override suspend fun analytics(): AdminAnalyticsDto = analyticsResponse

    override suspend fun users(limit: Int, search: String?): AdminUsersResponseDto = usersResponse

    override suspend fun updateUser(userId: Int, request: AdminUpdateUserRequestDto): AdminUserDto {
        lastUpdateUserId = userId
        lastUpdateRequest = request
        return updateUserResponse
    }

    override suspend fun deleteUser(userId: Int) {
        lastDeleteUserId = userId
    }
}

private class FailingAdminApi(private val statusCode: Int) : AdminApi {
    private fun fail(): Nothing = throw HttpException(
        Response.error<Any>(
            statusCode,
            """{"error":{"code":"ERROR","message":"Request failed."}}"""
                .toResponseBody("application/json".toMediaType()),
        ),
    )

    override suspend fun analytics(): AdminAnalyticsDto = fail()
    override suspend fun users(limit: Int, search: String?): AdminUsersResponseDto = fail()
    override suspend fun updateUser(userId: Int, request: AdminUpdateUserRequestDto): AdminUserDto = fail()
    override suspend fun deleteUser(userId: Int) = fail()
}

private class NetworkErrorAdminApi : AdminApi {
    private fun fail(): Nothing = throw IOException("Network unavailable")

    override suspend fun analytics(): AdminAnalyticsDto = fail()
    override suspend fun users(limit: Int, search: String?): AdminUsersResponseDto = fail()
    override suspend fun updateUser(userId: Int, request: AdminUpdateUserRequestDto): AdminUserDto = fail()
    override suspend fun deleteUser(userId: Int) = fail()
}
