package com.csnexus.app.feature.admin.ui

import com.csnexus.app.core.error.AppError
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.admin.data.AdminAnalyticsDto
import com.csnexus.app.feature.admin.data.AdminRepositoryContract
import com.csnexus.app.feature.admin.data.AdminUserDto
import com.csnexus.app.feature.admin.data.AdminUsersResponseDto
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.StandardTestDispatcher
import kotlinx.coroutines.test.advanceUntilIdle
import kotlinx.coroutines.test.resetMain
import kotlinx.coroutines.test.runTest
import kotlinx.coroutines.test.setMain
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Before
import org.junit.Test

@OptIn(ExperimentalCoroutinesApi::class)
class AdminViewModelTest {

    private val dispatcher = StandardTestDispatcher()

    @Before
    fun setUp() {
        Dispatchers.setMain(dispatcher)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    // ── Load ──────────────────────────────────────────────────────────────────

    @Test
    fun loadFetchesAnalyticsAndUsers() = runTest {
        val analytics = makeAnalyticsDto(totalUsers = 42)
        val users = listOf(makeUserDto(id = 1), makeUserDto(id = 2))
        val repo = FakeAdminRepository(analyticsResult = ApiResult.Success(analytics), usersResult = successUsers(users))
        val vm = AdminViewModel(repo, isAdmin = true, filterDispatcher = dispatcher)

        advanceUntilIdle()

        val state = vm.uiState.value
        assertEquals(42, state.analytics?.totalUsers)
        assertEquals(2, state.allUsers.size)
        assertEquals(2, state.filteredUsers.size)
        assertFalse(state.analyticsLoading)
        assertFalse(state.usersLoading)
    }

    // ── Search ────────────────────────────────────────────────────────────────

    @Test
    fun searchFiltersByEmail() = runTest {
        val users = listOf(makeUserDto(id = 1, email = "alice@example.com"), makeUserDto(id = 2, email = "bob@example.com"))
        val vm = makeVmWithUsers(users, dispatcher)
        advanceUntilIdle()

        vm.onSearchChanged("alice")
        advanceUntilIdle()

        assertEquals(1, vm.uiState.value.filteredUsers.size)
        assertEquals("alice@example.com", vm.uiState.value.filteredUsers.first().email)
    }

    @Test
    fun searchFiltersByDisplayName() = runTest {
        val users = listOf(makeUserDto(id = 1, displayName = "Alice Smith"), makeUserDto(id = 2, displayName = "Bob Jones"))
        val vm = makeVmWithUsers(users, dispatcher)
        advanceUntilIdle()

        vm.onSearchChanged("jones")
        advanceUntilIdle()

        assertEquals(1, vm.uiState.value.filteredUsers.size)
        assertEquals("Bob Jones", vm.uiState.value.filteredUsers.first().displayName)
    }

    @Test
    fun searchFiltersByUsername() = runTest {
        val users = listOf(makeUserDto(id = 1, username = "xalice"), makeUserDto(id = 2, username = "ybob"))
        val vm = makeVmWithUsers(users, dispatcher)
        advanceUntilIdle()

        vm.onSearchChanged("xalice")
        advanceUntilIdle()

        assertEquals(1, vm.uiState.value.filteredUsers.size)
        assertEquals("xalice", vm.uiState.value.filteredUsers.first().username)
    }

    @Test
    fun searchCaseInsensitive() = runTest {
        val users = listOf(makeUserDto(id = 1, email = "Alice@Example.com"))
        val vm = makeVmWithUsers(users, dispatcher)
        advanceUntilIdle()

        vm.onSearchChanged("ALICE")
        advanceUntilIdle()

        assertEquals(1, vm.uiState.value.filteredUsers.size)
    }

    @Test
    fun searchEmptyQueryShowsAll() = runTest {
        val users = listOf(makeUserDto(id = 1), makeUserDto(id = 2), makeUserDto(id = 3))
        val vm = makeVmWithUsers(users, dispatcher)
        advanceUntilIdle()

        vm.onSearchChanged("foo")
        advanceUntilIdle()
        assertEquals(0, vm.uiState.value.filteredUsers.size)

        vm.onSearchChanged("")
        advanceUntilIdle()
        assertEquals(3, vm.uiState.value.filteredUsers.size)
    }

    // ── Ban/Unban optimistic ──────────────────────────────────────────────────

    @Test
    fun toggleBanOptimisticallyFlipsBannedState() = runTest {
        val user = makeUserDto(id = 5, isBanned = false)
        val updatedUser = user.copy(isBanned = true)
        val repo = FakeAdminRepository(
            usersResult = successUsers(listOf(user)),
            banUserResult = ApiResult.Success(updatedUser),
        )
        val vm = AdminViewModel(repo, isAdmin = true, filterDispatcher = dispatcher)
        advanceUntilIdle()

        // Before server response, optimistic flip should already be visible
        vm.toggleBan(user)

        // Check optimistic state immediately (before advanceUntilIdle)
        assertTrue(vm.uiState.value.filteredUsers.first { it.id == 5 }.isBanned)

        advanceUntilIdle()

        // After server response, state should remain banned
        assertTrue(vm.uiState.value.filteredUsers.first { it.id == 5 }.isBanned)
    }

    @Test
    fun toggleBanRollsBackOnFailure() = runTest {
        val user = makeUserDto(id = 5, isBanned = false)
        val repo = FakeAdminRepository(
            usersResult = successUsers(listOf(user)),
            banUserResult = ApiResult.Failure(AppError.Network("Network error")),
        )
        val vm = AdminViewModel(repo, isAdmin = true, filterDispatcher = dispatcher)
        advanceUntilIdle()

        vm.toggleBan(user)
        advanceUntilIdle()

        // Rolled back to original state
        assertFalse(vm.uiState.value.filteredUsers.first { it.id == 5 }.isBanned)
    }

    @Test
    fun toggleBanSetsActionMessage() = runTest {
        val user = makeUserDto(id = 5, isBanned = false)
        val updatedUser = user.copy(isBanned = true)
        val repo = FakeAdminRepository(
            usersResult = successUsers(listOf(user)),
            banUserResult = ApiResult.Success(updatedUser),
        )
        val vm = AdminViewModel(repo, isAdmin = true, filterDispatcher = dispatcher)
        advanceUntilIdle()

        vm.toggleBan(user)
        advanceUntilIdle()

        assertNotNull(vm.uiState.value.actionMessage)
    }

    // ── Delete ────────────────────────────────────────────────────────────────

    @Test
    fun requestDeleteSetsDeleteTarget() = runTest {
        val user = makeUserDto(id = 9)
        val vm = makeVmWithUsers(listOf(user), dispatcher)
        advanceUntilIdle()

        vm.requestDelete(user)

        assertEquals(9, vm.uiState.value.deleteTarget?.id)
    }

    @Test
    fun confirmDeleteRemovesUserFromList() = runTest {
        val user = makeUserDto(id = 9)
        val repo = FakeAdminRepository(
            usersResult = successUsers(listOf(user, makeUserDto(id = 10))),
            deleteUserResult = ApiResult.Success(Unit),
        )
        val vm = AdminViewModel(repo, isAdmin = true, filterDispatcher = dispatcher)
        advanceUntilIdle()

        vm.requestDelete(user)
        vm.confirmDelete()
        advanceUntilIdle()

        assertEquals(1, vm.uiState.value.allUsers.size)
        assertEquals(10, vm.uiState.value.allUsers.first().id)
        assertNull(vm.uiState.value.deleteTarget)
    }

    @Test
    fun confirmDeleteRefreshesAnalytics() = runTest {
        val user = makeUserDto(id = 9)
        var analyticsCallCount = 0
        val repo = FakeAdminRepository(
            analyticsResult = ApiResult.Success(makeAnalyticsDto(totalUsers = 50)),
            usersResult = successUsers(listOf(user)),
            deleteUserResult = ApiResult.Success(Unit),
            onAnalytics = { analyticsCallCount++ },
        )
        val vm = AdminViewModel(repo, isAdmin = true, filterDispatcher = dispatcher)
        advanceUntilIdle()

        val initialAnalyticsCallCount = analyticsCallCount

        vm.requestDelete(user)
        vm.confirmDelete()
        advanceUntilIdle()

        // Analytics should be fetched once at init and again after delete
        assertTrue(analyticsCallCount > initialAnalyticsCallCount)
    }

    @Test
    fun confirmDeleteFailureSetsErrorMessage() = runTest {
        val user = makeUserDto(id = 9)
        val repo = FakeAdminRepository(
            usersResult = successUsers(listOf(user)),
            deleteUserResult = ApiResult.Failure(AppError.Http(500, "ERROR", "Server error", null)),
        )
        val vm = AdminViewModel(repo, isAdmin = true, filterDispatcher = dispatcher)
        advanceUntilIdle()

        vm.requestDelete(user)
        vm.confirmDelete()
        advanceUntilIdle()

        assertNotNull(vm.uiState.value.errorMessage)
        assertNull(vm.uiState.value.deleteTarget)
    }

    @Test
    fun dismissDeleteClearsTarget() = runTest {
        val user = makeUserDto(id = 9)
        val vm = makeVmWithUsers(listOf(user), dispatcher)
        advanceUntilIdle()

        vm.requestDelete(user)
        assertNotNull(vm.uiState.value.deleteTarget)

        vm.dismissDelete()
        assertNull(vm.uiState.value.deleteTarget)
    }

    // ── clearActionMessage ────────────────────────────────────────────────────

    @Test
    fun clearActionMessageNullsField() = runTest {
        val user = makeUserDto(id = 5, isBanned = false)
        val updatedUser = user.copy(isBanned = true)
        val repo = FakeAdminRepository(
            usersResult = successUsers(listOf(user)),
            banUserResult = ApiResult.Success(updatedUser),
        )
        val vm = AdminViewModel(repo, isAdmin = true, filterDispatcher = dispatcher)
        advanceUntilIdle()

        vm.toggleBan(user)
        advanceUntilIdle()
        assertNotNull(vm.uiState.value.actionMessage)

        vm.clearActionMessage()
        assertNull(vm.uiState.value.actionMessage)
    }

    // ── Non-admin blocks load ─────────────────────────────────────────────────

    @Test
    fun nonAdminBlocksLoad() = runTest {
        val repo = FakeAdminRepository(
            analyticsResult = ApiResult.Success(makeAnalyticsDto(totalUsers = 999)),
            usersResult = successUsers(listOf(makeUserDto(id = 1))),
        )
        val vm = AdminViewModel(repo, isAdmin = false, filterDispatcher = dispatcher)
        advanceUntilIdle()

        // ViewModel should not expose any admin data when isAdmin = false
        assertNull(vm.uiState.value.analytics)
        assertTrue(vm.uiState.value.allUsers.isEmpty())
    }
}

// ── Helpers ───────────────────────────────────────────────────────────────────

private fun makeAnalyticsDto(totalUsers: Int = 0) = AdminAnalyticsDto(
    totalUsers = totalUsers,
    verifiedUsers = 0,
    bannedUsers = 0,
    totalLessonsCompleted = 0,
    totalQuizAttempts = 0,
    totalMockAttempts = 0,
    mockPassRate = 0.0,
    weakestSubtopics = emptyList(),
)

private fun makeUserDto(
    id: Int = 1,
    email: String = "user$id@example.com",
    displayName: String = "User $id",
    username: String? = "user$id",
    isBanned: Boolean = false,
) = AdminUserDto(
    id = id,
    email = email,
    displayName = displayName,
    username = username,
    role = "user",
    isBanned = isBanned,
)

private fun successUsers(users: List<AdminUserDto>) =
    ApiResult.Success(AdminUsersResponseDto(items = users, total = users.size))

private fun makeVmWithUsers(
    users: List<AdminUserDto>,
    dispatcher: CoroutineDispatcher,
): AdminViewModel {
    val repo = FakeAdminRepository(usersResult = successUsers(users))
    return AdminViewModel(
        repository = repo,
        isAdmin = true,
        filterDispatcher = dispatcher,
    )
}

// ── Fake repository ───────────────────────────────────────────────────────────

private class FakeAdminRepository(
    private val analyticsResult: ApiResult<AdminAnalyticsDto> = ApiResult.Success(makeAnalyticsDto()),
    private val usersResult: ApiResult<AdminUsersResponseDto> = ApiResult.Success(
        AdminUsersResponseDto(items = emptyList(), total = 0),
    ),
    private val banUserResult: ApiResult<AdminUserDto> = ApiResult.Success(makeUserDto(isBanned = true)),
    private val unbanUserResult: ApiResult<AdminUserDto> = ApiResult.Success(makeUserDto(isBanned = false)),
    private val deleteUserResult: ApiResult<Unit> = ApiResult.Success(Unit),
    private val onAnalytics: (() -> Unit)? = null,
) : AdminRepositoryContract {

    override suspend fun analytics(): ApiResult<AdminAnalyticsDto> {
        onAnalytics?.invoke()
        return analyticsResult
    }

    override suspend fun users(search: String?): ApiResult<AdminUsersResponseDto> = usersResult

    override suspend fun banUser(userId: Int): ApiResult<AdminUserDto> = banUserResult

    override suspend fun unbanUser(userId: Int): ApiResult<AdminUserDto> = unbanUserResult

    override suspend fun deleteUser(userId: Int): ApiResult<Unit> = deleteUserResult
}
