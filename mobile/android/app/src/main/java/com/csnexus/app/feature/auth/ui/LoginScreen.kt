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
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccountCircle
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
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.csnexus.app.core.auth.AuthRepository
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.CSNexusDesign
import com.csnexus.app.core.design.CSNexusSegmentedControl
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.GlassLarge
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.design.rememberCSNexusReducedMotion
import com.csnexus.app.feature.auth.data.GoogleSignInClient
import com.csnexus.app.feature.auth.data.GoogleSignInResult
import kotlinx.coroutines.launch

@Composable
fun LoginScreen(
    authRepository: AuthRepository,
    googleServerClientId: String,
    onAuthenticated: () -> Unit,
    onSignup: () -> Unit,
    onForgotPassword: () -> Unit,
    viewModel: AuthViewModel = viewModel(factory = AuthViewModelFactory(authRepository)),
) {
    val state by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()
    var showEmailForm by remember { mutableStateOf(false) }
    val googleSignInClient = remember(context, googleServerClientId) {
        GoogleSignInClient(context, googleServerClientId)
    }

    // Entry animation: scale from 0.95→1 + fade
    val reducedMotion = rememberCSNexusReducedMotion()
    var visible by remember { mutableStateOf(reducedMotion) }
    LaunchedEffect(Unit) { visible = true }
    val scale by animateFloatAsState(
        targetValue = if (visible) 1f else 0.95f,
        animationSpec = if (reducedMotion) snap() else tween(durationMillis = 400),
        label = "login_scale",
    )
    val alpha by animateFloatAsState(
        targetValue = if (visible) 1f else 0f,
        animationSpec = if (reducedMotion) snap() else tween(durationMillis = 400),
        label = "login_alpha",
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
                        text = "Welcome back",
                        style = MaterialTheme.typography.headlineLarge,
                    )

                    // Subtitle
                    Text(
                        "Sign in to continue your prep",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )

                    Spacer(Modifier.height(8.dp))

                    // Google sign-in button first
                    CSNexusButton(
                        text = if (state.googleCategoryRequired) "Continue with Google" else "Sign in with Google",
                        onClick = {
                            coroutineScope.launch {
                                if (state.googleCategoryRequired) {
                                    viewModel.loginWithGoogle(
                                        androidPackage = context.packageName,
                                        onAuthenticated = onAuthenticated,
                                    )
                                } else {
                                    when (val result = googleSignInClient.signInWithGoogleButton()) {
                                        is GoogleSignInResult.Success -> {
                                            viewModel.onGoogleIdTokenReceived(result.idToken)
                                            viewModel.loginWithGoogle(
                                                androidPackage = context.packageName,
                                                onAuthenticated = onAuthenticated,
                                            )
                                        }
                                        is GoogleSignInResult.Failure -> {
                                            viewModel.onGoogleSignInFailed(result.userMessage)
                                        }
                                    }
                                }
                            }
                        },
                        enabled = !state.isGoogleLoading && !state.isLoading,
                        loading = state.isGoogleLoading,
                        variant = CSNexusButtonVariant.Secondary,
                        leadingIcon = {
                            androidx.compose.material3.Icon(
                                imageVector = Icons.Filled.AccountCircle,
                                contentDescription = null,
                            )
                        },
                        modifier = Modifier.fillMaxWidth(),
                    )

                    if (state.googleCategoryRequired) {
                        Text(
                            text = "Choose your category to finish Google sign-in.",
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                        CSNexusSegmentedControl(
                            options = authCategoryLabels,
                            selectedIndex = state.googleCategoryIndex,
                            onSelected = viewModel::onGoogleCategorySelected,
                        )
                    }

                    // "or" divider: thin line + centered "or" text
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

                    // Email form
                    if (showEmailForm || state.email.isNotBlank() || state.password.isNotBlank() || state.errorMessage != null) {
                        CSNexusTextField(
                            value = state.email,
                            onValueChange = viewModel::onEmailChanged,
                            label = "Email",
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                        )
                        CSNexusTextField(
                            value = state.password,
                            onValueChange = viewModel::onPasswordChanged,
                            label = "Password",
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                            isError = state.errorMessage != null,
                        )

                        // Error: danger-tinted glass pill
                        if (state.errorMessage != null) {
                            Surface(
                                color = CSNexusDesign.tokens.semantic.danger.copy(alpha = 0.10f),
                                border = BorderStroke(1.dp, CSNexusDesign.tokens.semantic.danger.copy(alpha = 0.35f)),
                                shape = RoundedCornerShape(999.dp),
                            ) {
                                Text(
                                    text = state.errorMessage.orEmpty(),
                                    modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                                    color = CSNexusDesign.tokens.semantic.danger,
                                    style = MaterialTheme.typography.bodySmall,
                                )
                            }
                        }

                        // Full-width primary button
                        CSNexusButton(
                            text = "Sign in",
                            onClick = { viewModel.login(onAuthenticated) },
                            enabled = !state.isLoading && !state.isGoogleLoading,
                            loading = state.isLoading,
                            modifier = Modifier.fillMaxWidth(),
                        )
                    } else {
                        CSNexusButton(
                            text = "Continue with Email",
                            onClick = { showEmailForm = true },
                            variant = CSNexusButtonVariant.Secondary,
                            enabled = !state.isLoading && !state.isGoogleLoading,
                            modifier = Modifier.fillMaxWidth(),
                        )
                    }

                    Spacer(modifier = Modifier.height(4.dp))

                    TextButton(onClick = onForgotPassword, modifier = Modifier.fillMaxWidth()) {
                        Text("Forgot password?")
                    }

                    TextButton(onClick = onSignup, modifier = Modifier.fillMaxWidth()) {
                        Text("Create account")
                    }
                }
            }
        }
    }
}
