package com.csnexus.app.feature.auth.ui

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.snap
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import androidx.lifecycle.viewmodel.compose.viewModel
import com.csnexus.app.core.auth.AuthRepository
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusDesign
import com.csnexus.app.core.design.CSNexusOtpField
import com.csnexus.app.core.design.CSNexusSegmentedControl
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.GlassLarge
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.design.rememberCSNexusReducedMotion
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.network.ApiResult
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class SignupUiState(
    val email: String = "",
    val displayName: String = "",
    val username: String = "",
    val password: String = "",
    val age: String = "",
    val categoryIndex: Int = 0,
    val isLoading: Boolean = false,
    val errorMessage: String? = null,
)

data class ForgotPasswordUiState(
    val email: String = "",
    val isLoading: Boolean = false,
    val submitted: Boolean = false,
    val errorMessage: String? = null,
)

data class OtpUiState(
    val code: String = "",
    val newPassword: String = "",
    val isLoading: Boolean = false,
    val errorMessage: String? = null,
)

class SignupViewModel(private val authRepository: AuthRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(SignupUiState())
    val uiState: StateFlow<SignupUiState> = _uiState.asStateFlow()

    fun onEmailChanged(value: String) = update { it.copy(email = value, errorMessage = null) }
    fun onDisplayNameChanged(value: String) = update { it.copy(displayName = value, errorMessage = null) }
    fun onUsernameChanged(value: String) = update { it.copy(username = value, errorMessage = null) }
    fun onPasswordChanged(value: String) = update { it.copy(password = value, errorMessage = null) }
    fun onAgeChanged(value: String) = update { it.copy(age = value.filter(Char::isDigit).take(3), errorMessage = null) }
    fun onCategorySelected(index: Int) = update { it.copy(categoryIndex = index, errorMessage = null) }

    fun signup(onOtpRequired: (String) -> Unit) {
        val state = _uiState.value
        val age = state.age.toIntOrNull()
        val error = validateSignup(state, age)
        if (error != null) {
            update { it.copy(errorMessage = error) }
            return
        }

        viewModelScope.launch {
            update { it.copy(isLoading = true, errorMessage = null) }
            when (
                val result = authRepository.signup(
                    email = state.email.trim(),
                    displayName = state.displayName.trim(),
                    username = state.username.trim(),
                    password = state.password,
                    age = age ?: 0,
                    category = authCategoryValues[state.categoryIndex],
                )
            ) {
                is ApiResult.Success -> {
                    update { it.copy(isLoading = false) }
                    onOtpRequired(state.email.trim())
                }
                is ApiResult.Failure -> update {
                    it.copy(isLoading = false, errorMessage = result.error.userMessage())
                }
            }
        }
    }

    private fun update(block: (SignupUiState) -> SignupUiState) {
        _uiState.update(block)
    }

    private fun validateSignup(state: SignupUiState, age: Int?): String? = when {
        state.email.isBlank() -> "Email is required."
        state.displayName.isBlank() -> "Display name is required."
        state.username.length < 3 -> "Username must be at least 3 characters."
        state.password.length < 8 -> "Password must be at least 8 characters."
        age == null || age !in 15..100 -> "Age must be between 15 and 100."
        else -> null
    }
}

class ForgotPasswordViewModel(private val authRepository: AuthRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(ForgotPasswordUiState())
    val uiState: StateFlow<ForgotPasswordUiState> = _uiState.asStateFlow()

    fun onEmailChanged(value: String) {
        _uiState.update { it.copy(email = value, errorMessage = null) }
    }

    fun requestReset() {
        val email = _uiState.value.email.trim()
        if (email.isBlank()) {
            _uiState.update { it.copy(errorMessage = "Email is required.") }
            return
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, errorMessage = null) }
            authRepository.requestPasswordReset(email)
            _uiState.update { it.copy(isLoading = false, submitted = true) }
        }
    }
}

class OtpViewModel(private val authRepository: AuthRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(OtpUiState())
    val uiState: StateFlow<OtpUiState> = _uiState.asStateFlow()

    fun onCodeChanged(value: String) {
        _uiState.update { it.copy(code = value, errorMessage = null) }
    }

    fun onNewPasswordChanged(value: String) {
        _uiState.update { it.copy(newPassword = value, errorMessage = null) }
    }

    fun verifyEmail(email: String, onVerified: (Boolean) -> Unit) {
        val code = _uiState.value.code
        if (email.isBlank() || code.length != 6) {
            _uiState.update { it.copy(errorMessage = "Enter the 6-digit verification code.") }
            return
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, errorMessage = null) }
            when (val result = authRepository.verifyEmail(email, code)) {
                is ApiResult.Success -> {
                    _uiState.update { it.copy(isLoading = false) }
                    onVerified(authRepository.isAuthenticated())
                }
                is ApiResult.Failure -> _uiState.update {
                    it.copy(isLoading = false, errorMessage = result.error.userMessage())
                }
            }
        }
    }

    fun resetPassword(email: String, onReset: () -> Unit) {
        val state = _uiState.value
        if (email.isBlank() || state.code.length != 6 || state.newPassword.length < 8) {
            _uiState.update { it.copy(errorMessage = "Enter the code and a new password of at least 8 characters.") }
            return
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, errorMessage = null) }
            when (val result = authRepository.resetPassword(email, state.code, state.newPassword)) {
                is ApiResult.Success -> {
                    _uiState.update { it.copy(isLoading = false) }
                    onReset()
                }
                is ApiResult.Failure -> _uiState.update {
                    it.copy(isLoading = false, errorMessage = result.error.userMessage())
                }
            }
        }
    }
}

@Composable
fun SignupScreen(
    authRepository: AuthRepository,
    onOtpRequired: (String) -> Unit,
    onLogin: () -> Unit,
    viewModel: SignupViewModel = viewModel(factory = SimpleAuthViewModelFactory { SignupViewModel(authRepository) }),
) {
    val state by viewModel.uiState.collectAsState()

    AuthCard(title = "Create account", subtitle = "Start your CSE prep journey") {
        CSNexusTextField(state.email, viewModel::onEmailChanged, "Email", keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email))
        CSNexusTextField(state.displayName, viewModel::onDisplayNameChanged, "Display name")
        CSNexusTextField(state.username, viewModel::onUsernameChanged, "Username")
        CSNexusTextField(
            value = state.password,
            onValueChange = viewModel::onPasswordChanged,
            label = "Password",
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
            visualTransformation = PasswordVisualTransformation(),
            supportingText = "Min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special character",
        )
        CSNexusTextField(state.age, viewModel::onAgeChanged, "Age", keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number))
        CSNexusSegmentedControl(authCategoryLabels, state.categoryIndex, viewModel::onCategorySelected)

        // "or" divider between form sections
        OrDivider()

        AuthError(state.errorMessage)
        CSNexusButton(
            text = "Sign up",
            onClick = { viewModel.signup(onOtpRequired) },
            loading = state.isLoading,
            modifier = Modifier.fillMaxWidth(),
        )
        TextButton(onClick = onLogin, modifier = Modifier.fillMaxWidth()) {
            Text("Already have an account? Log in")
        }
    }
}

@Composable
fun ForgotPasswordScreen(
    authRepository: AuthRepository,
    onEnterCode: (String) -> Unit,
    onLogin: () -> Unit,
    viewModel: ForgotPasswordViewModel = viewModel(factory = SimpleAuthViewModelFactory { ForgotPasswordViewModel(authRepository) }),
) {
    val state by viewModel.uiState.collectAsState()

    AuthCard(
        title = if (state.submitted) "Check your email" else "Forgot password",
        subtitle = if (state.submitted) {
            "If an account exists for ${state.email}, we sent a password reset code."
        } else {
            "Enter your email and we will send a reset code."
        },
    ) {
        if (!state.submitted) {
            CSNexusTextField(state.email, viewModel::onEmailChanged, "Email", keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email))
            AuthError(state.errorMessage)
            CSNexusButton(
                text = "Send reset code",
                onClick = viewModel::requestReset,
                loading = state.isLoading,
                modifier = Modifier.fillMaxWidth(),
            )
        } else {
            CSNexusButton(
                text = "Enter code",
                onClick = { onEnterCode(state.email.trim()) },
                modifier = Modifier.fillMaxWidth(),
            )
        }
        TextButton(onClick = onLogin, modifier = Modifier.fillMaxWidth()) {
            Text("Back to login")
        }
    }
}

@Composable
fun OtpVerificationScreen(
    authRepository: AuthRepository,
    email: String,
    purpose: String,
    onAuthenticated: () -> Unit,
    onLogin: () -> Unit,
    viewModel: OtpViewModel = viewModel(factory = SimpleAuthViewModelFactory { OtpViewModel(authRepository) }),
) {
    val state by viewModel.uiState.collectAsState()
    val isPasswordReset = purpose == "PASSWORD_RESET"

    AuthCard(
        title = if (isPasswordReset) "Reset password" else "Verify email",
        subtitle = "Enter the 6-digit code sent to ${email.ifBlank { "your email" }}.",
    ) {
        CSNexusOtpField(state.code, viewModel::onCodeChanged)
        if (isPasswordReset) {
            CSNexusTextField(
                value = state.newPassword,
                onValueChange = viewModel::onNewPasswordChanged,
                label = "New password",
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                visualTransformation = PasswordVisualTransformation(),
            )
        }
        AuthError(state.errorMessage)
        CSNexusButton(
            text = if (isPasswordReset) "Reset password" else "Verify",
            onClick = {
                if (isPasswordReset) {
                    viewModel.resetPassword(email, onLogin)
                } else {
                    viewModel.verifyEmail(email) { authenticated ->
                        if (authenticated) onAuthenticated() else onLogin()
                    }
                }
            },
            loading = state.isLoading,
            modifier = Modifier.fillMaxWidth(),
        )
        TextButton(onClick = onLogin, modifier = Modifier.fillMaxWidth()) {
            Text("Back to login")
        }
    }
}

@Composable
private fun AuthCard(
    title: String,
    subtitle: String,
    content: @Composable () -> Unit,
) {
    // Entry animation: scale from 0.95→1 + fade
    val reducedMotion = rememberCSNexusReducedMotion()
    var visible by remember { mutableStateOf(reducedMotion) }
    LaunchedEffect(Unit) { visible = true }
    val scale by animateFloatAsState(
        targetValue = if (visible) 1f else 0.95f,
        animationSpec = if (reducedMotion) snap() else tween(durationMillis = 400),
        label = "auth_card_scale",
    )
    val alpha by animateFloatAsState(
        targetValue = if (visible) 1f else 0f,
        animationSpec = if (reducedMotion) snap() else tween(durationMillis = 400),
        label = "auth_card_alpha",
    )

    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center,
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .verticalScroll(rememberScrollState())
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
        ) {
            GlassLarge(
                modifier = Modifier
                    .widthIn(max = 420.dp)
                    .graphicsLayer {
                        scaleX = scale
                        scaleY = scale
                    }
                    .alpha(alpha),
            ) {
                Column(
                    modifier = Modifier.padding(40.dp),
                    verticalArrangement = Arrangement.spacedBy(12.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                ) {
                    // Logo emoji
                    Text(
                        text = "\uD83C\uDF93",
                        fontSize = 48.sp,
                    )

                    // Metallic gradient heading
                    MetallicText(
                        text = title,
                        style = MaterialTheme.typography.headlineLarge,
                    )

                    // Subtitle in secondary
                    Text(
                        text = subtitle,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )

                    Spacer(Modifier.height(8.dp))
                    content()
                }
            }
        }
    }
}

@Composable
private fun OrDivider() {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        HorizontalDivider(
            modifier = Modifier.weight(1f),
            color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f),
        )
        Text(
            text = "or",
            modifier = Modifier.padding(horizontal = 12.dp),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            style = MaterialTheme.typography.bodySmall,
        )
        HorizontalDivider(
            modifier = Modifier.weight(1f),
            color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.3f),
        )
    }
}

@Composable
private fun AuthError(message: String?) {
    if (message != null) {
        Surface(
            color = CSNexusDesign.tokens.semantic.danger.copy(alpha = 0.10f),
            border = BorderStroke(1.dp, CSNexusDesign.tokens.semantic.danger.copy(alpha = 0.35f)),
            shape = RoundedCornerShape(999.dp),
        ) {
            Text(
                text = message,
                modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                color = CSNexusDesign.tokens.semantic.danger,
                style = MaterialTheme.typography.bodySmall,
            )
        }
    }
}

private class SimpleAuthViewModelFactory<T : ViewModel>(
    private val create: () -> T,
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <VM : ViewModel> create(modelClass: Class<VM>): VM = create() as VM
}
