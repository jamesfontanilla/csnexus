package com.csnexus.app.feature.auth.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.csnexus.app.core.auth.AuthRepository
import com.csnexus.app.core.error.AppError
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.network.ApiResult
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class LoginUiState(
    val email: String = "",
    val password: String = "",
    val googleCategoryIndex: Int = 0,
    val pendingGoogleIdToken: String? = null,
    val googleCategoryRequired: Boolean = false,
    val isLoading: Boolean = false,
    val isGoogleLoading: Boolean = false,
    val errorMessage: String? = null,
)

class AuthViewModel(
    private val authRepository: AuthRepository,
) : ViewModel() {
    private val _uiState = MutableStateFlow(LoginUiState())
    val uiState: StateFlow<LoginUiState> = _uiState.asStateFlow()

    fun onEmailChanged(value: String) {
        _uiState.update { it.copy(email = value, errorMessage = null) }
    }

    fun onPasswordChanged(value: String) {
        _uiState.update { it.copy(password = value, errorMessage = null) }
    }

    fun onGoogleCategorySelected(index: Int) {
        _uiState.update { it.copy(googleCategoryIndex = index, errorMessage = null) }
    }

    fun onGoogleIdTokenReceived(idToken: String) {
        _uiState.update {
            it.copy(
                pendingGoogleIdToken = idToken,
                googleCategoryRequired = false,
                errorMessage = null,
            )
        }
    }

    fun onGoogleSignInFailed(message: String) {
        _uiState.update { it.copy(errorMessage = message) }
    }

    fun login(onAuthenticated: () -> Unit) {
        val state = _uiState.value
        if (state.email.isBlank() || state.password.isBlank()) {
            _uiState.update { it.copy(errorMessage = "Email and password are required.") }
            return
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, errorMessage = null) }
            when (val result = authRepository.login(state.email.trim(), state.password)) {
                is ApiResult.Success -> {
                    _uiState.update { it.copy(isLoading = false) }
                    onAuthenticated()
                }
                is ApiResult.Failure -> {
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            errorMessage = result.error.userMessage(),
                        )
                    }
                }
            }
        }
    }

    fun loginWithGoogle(
        androidPackage: String,
        onAuthenticated: () -> Unit,
    ) {
        val state = _uiState.value
        val idToken = state.pendingGoogleIdToken
        if (idToken.isNullOrBlank()) {
            _uiState.update {
                it.copy(errorMessage = "Google sign-in needs to be started again.")
            }
            return
        }

        val category = if (state.googleCategoryRequired) {
            authCategoryValues[state.googleCategoryIndex]
        } else {
            null
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isGoogleLoading = true, errorMessage = null) }
            when (
                val result = authRepository.loginWithGoogle(
                    idToken = idToken,
                    androidPackage = androidPackage,
                    category = category,
                )
            ) {
                is ApiResult.Success -> {
                    _uiState.update {
                        it.copy(
                            isGoogleLoading = false,
                            pendingGoogleIdToken = null,
                            googleCategoryRequired = false,
                            googleCategoryIndex = 0,
                            errorMessage = null,
                        )
                    }
                    onAuthenticated()
                }
                is ApiResult.Failure -> {
                    val isCategoryRequired = result.error is AppError.Http &&
                        result.error.statusCode == 422 &&
                        result.error.message == "category_required"
                    _uiState.update {
                        it.copy(
                            isGoogleLoading = false,
                            googleCategoryRequired = isCategoryRequired,
                            pendingGoogleIdToken = if (isCategoryRequired) idToken else null,
                            errorMessage = if (isCategoryRequired) {
                                "Choose a category to finish signing in with Google."
                            } else {
                                result.error.userMessage()
                            },
                        )
                    }
                }
            }
        }
    }
}

class AuthViewModelFactory(
    private val authRepository: AuthRepository,
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return AuthViewModel(authRepository) as T
    }
}
