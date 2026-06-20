package com.csnexus.app.feature.admin.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.admin.data.AdminAnalyticsDto
import com.csnexus.app.feature.admin.data.AdminRepositoryContract
import com.csnexus.app.feature.admin.data.AdminUserDto
import kotlinx.coroutines.CoroutineDispatcher
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

data class AdminUiState(
    val analytics: AdminAnalyticsDto? = null,
    val allUsers: List<AdminUserDto> = emptyList(),
    val filteredUsers: List<AdminUserDto> = emptyList(),
    val searchQuery: String = "",
    val analyticsLoading: Boolean = false,
    val usersLoading: Boolean = false,
    val errorMessage: String? = null,
    val deleteTarget: AdminUserDto? = null,
    val isDeleting: Boolean = false,
    val actionMessage: String? = null,
)

class AdminViewModel(
    private val repository: AdminRepositoryContract,
    private val isAdmin: Boolean,
    private val filterDispatcher: CoroutineDispatcher = Dispatchers.Default,
) : ViewModel() {

    private val _uiState = MutableStateFlow(AdminUiState())
    val uiState: StateFlow<AdminUiState> = _uiState.asStateFlow()

    init {
        if (isAdmin) load()
    }

    fun load() {
        if (!isAdmin) return
        viewModelScope.launch {
            _uiState.update { it.copy(analyticsLoading = true, usersLoading = true, errorMessage = null) }

            val analyticsDeferred = async { repository.analytics() }
            val usersDeferred = async { repository.users() }

            val analyticsResult = analyticsDeferred.await()
            val usersResult = usersDeferred.await()

            val analytics = when (analyticsResult) {
                is ApiResult.Success -> analyticsResult.value
                is ApiResult.Failure -> {
                    _uiState.update { it.copy(errorMessage = "Could not load admin analytics.") }
                    null
                }
            }

            val users = when (usersResult) {
                is ApiResult.Success -> usersResult.value.items
                is ApiResult.Failure -> {
                    _uiState.update { it.copy(errorMessage = "Could not load user list.") }
                    emptyList()
                }
            }

            val filtered = filterUsersAsync(users, _uiState.value.searchQuery)
            _uiState.update {
                it.copy(
                    analytics = analytics ?: it.analytics,
                    allUsers = users,
                    filteredUsers = filtered,
                    analyticsLoading = false,
                    usersLoading = false,
                )
            }
        }
    }

    fun onSearchChanged(query: String) {
        _uiState.update { it.copy(searchQuery = query) }
        viewModelScope.launch {
            val users = _uiState.value.allUsers
            val filtered = filterUsersAsync(users, query)
            _uiState.update { state ->
                if (state.searchQuery == query) {
                    state.copy(filteredUsers = filtered)
                } else {
                    state
                }
            }
        }
    }

    fun toggleBan(user: AdminUserDto) {
        val currentUsers = _uiState.value.allUsers
        // Optimistic flip
        val optimisticUsers = currentUsers.map { u ->
            if (u.id == user.id) u.copy(isBanned = !u.isBanned) else u
        }
        _uiState.update { state ->
            state.copy(
                allUsers = optimisticUsers,
                filteredUsers = if (state.searchQuery.isBlank()) {
                    optimisticUsers
                } else {
                    state.filteredUsers.map { existing ->
                        if (existing.id == user.id) existing.copy(isBanned = !existing.isBanned) else existing
                    }
                },
            )
        }
        viewModelScope.launch {
            val filtered = filterUsersAsync(optimisticUsers, _uiState.value.searchQuery)
            _uiState.update { state -> state.copy(filteredUsers = filtered) }
        }

        viewModelScope.launch {
            val result = if (user.isBanned) {
                repository.unbanUser(user.id)
            } else {
                repository.banUser(user.id)
            }
            when (result) {
                is ApiResult.Success -> {
                    val updated = result.value
                    val serverUsers = _uiState.value.allUsers.map { u ->
                        if (u.id == updated.id) updated else u
                    }
                    val filtered = filterUsersAsync(serverUsers, _uiState.value.searchQuery)
                    _uiState.update { state ->
                        state.copy(
                            allUsers = serverUsers,
                            filteredUsers = filtered,
                            actionMessage = if (updated.isBanned) "User banned." else "User unbanned.",
                        )
                    }
                }
                is ApiResult.Failure -> {
                    // Rollback: restore the original user list
                    val filtered = filterUsersAsync(currentUsers, _uiState.value.searchQuery)
                    _uiState.update { state ->
                        state.copy(
                            allUsers = currentUsers,
                            filteredUsers = filtered,
                            actionMessage = "Action failed. Please try again.",
                        )
                    }
                }
            }
        }
    }

    fun requestDelete(user: AdminUserDto) {
        _uiState.update { it.copy(deleteTarget = user) }
    }

    fun confirmDelete() {
        val target = _uiState.value.deleteTarget ?: return
        _uiState.update { it.copy(isDeleting = true) }

        viewModelScope.launch {
            when (repository.deleteUser(target.id)) {
                is ApiResult.Success -> {
                    val remaining = _uiState.value.allUsers.filter { it.id != target.id }
                    val filtered = filterUsersAsync(remaining, _uiState.value.searchQuery)
                    _uiState.update { state ->
                        state.copy(
                            allUsers = remaining,
                            filteredUsers = filtered,
                            deleteTarget = null,
                            isDeleting = false,
                            actionMessage = "User deleted.",
                        )
                    }
                    // Refresh analytics after delete
                    when (val analyticsResult = repository.analytics()) {
                        is ApiResult.Success -> _uiState.update { it.copy(analytics = analyticsResult.value) }
                        is ApiResult.Failure -> { /* best-effort; don't show a secondary error */ }
                    }
                }
                is ApiResult.Failure -> {
                    _uiState.update { state ->
                        state.copy(
                            deleteTarget = null,
                            isDeleting = false,
                            errorMessage = "Delete failed. Please try again.",
                        )
                    }
                }
            }
        }
    }

    fun dismissDelete() {
        _uiState.update { it.copy(deleteTarget = null) }
    }

    fun clearActionMessage() {
        _uiState.update { it.copy(actionMessage = null) }
    }

    fun clearErrorMessage() {
        _uiState.update { it.copy(errorMessage = null) }
    }

    // ── Private helpers ───────────────────────────────────────────────────────

    private suspend fun filterUsersAsync(users: List<AdminUserDto>, query: String): List<AdminUserDto> {
        return withContext(filterDispatcher) { filterUsers(users, query) }
    }

    private fun filterUsers(users: List<AdminUserDto>, query: String): List<AdminUserDto> {
        if (query.isBlank()) return users
        val normalizedQuery = query.trim().lowercase()
        return users.filter { user ->
            user.email.lowercase().contains(normalizedQuery) ||
                user.displayName.lowercase().contains(normalizedQuery) ||
                user.username?.lowercase()?.contains(normalizedQuery) == true
        }
    }
}

// ── Factory ───────────────────────────────────────────────────────────────────

class AdminViewModelFactory(
    private val repository: AdminRepositoryContract,
    private val isAdmin: Boolean,
    private val filterDispatcher: CoroutineDispatcher = Dispatchers.Default,
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return AdminViewModel(repository, isAdmin, filterDispatcher) as T
    }
}
