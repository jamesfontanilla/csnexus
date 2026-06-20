package com.csnexus.app.feature.settings.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.auth.AuthRepository
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.CSNexusOfflineBanner
import com.csnexus.app.core.design.CSNexusRetryPanel
import com.csnexus.app.core.design.CSNexusSegmentedControl
import com.csnexus.app.core.design.CSNexusStatusBadge
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.GlassMedium
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.auth.data.UserDto
import com.csnexus.app.feature.settings.data.SettingsPreferences
import com.csnexus.app.feature.settings.data.SettingsRepository
import com.csnexus.app.feature.settings.domain.DELETE_ACCOUNT_CONFIRMATION
import com.csnexus.app.feature.settings.domain.isValidDailyGoalMinutes
import com.csnexus.app.feature.settings.domain.isValidDailyGoalXp
import com.csnexus.app.feature.settings.domain.isValidPassword
import kotlinx.coroutines.launch
import kotlin.math.roundToInt

private val GoldActive = Color(0xFFC9A84C)
private val GoldActiveTrack = Color(0x66C9A84C) // 40% alpha gold

@Composable
fun SettingsScreen(
    authRepository: AuthRepository,
    settingsRepository: SettingsRepository,
    contentPadding: PaddingValues,
    onLoggedOut: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    val syncBannerFlow = settingsRepository.syncBanner()
    val syncBanner by (syncBannerFlow?.collectAsState(initial = null) ?: remember { mutableStateOf(null) })
    var user by remember { mutableStateOf<UserDto?>(null) }
    var preferences by remember { mutableStateOf(SettingsPreferences()) }
    var loading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var displayName by remember { mutableStateOf("") }
    var timezone by remember { mutableStateOf("Asia/Manila") }
    var profileMessage by remember { mutableStateOf<String?>(null) }
    var savingProfile by remember { mutableStateOf(false) }
    var targetXp by remember { mutableStateOf("50") }
    var targetMessage by remember { mutableStateOf<String?>(null) }
    var savingTarget by remember { mutableStateOf(false) }
    var currentPassword by remember { mutableStateOf("") }
    var newPassword by remember { mutableStateOf("") }
    var passwordMessage by remember { mutableStateOf<String?>(null) }
    var changingPassword by remember { mutableStateOf(false) }
    var showDeleteDialog by remember { mutableStateOf(false) }

    fun savePreferences(next: SettingsPreferences) {
        preferences = next
        scope.launch {
            settingsRepository.saveLocalPreferences(next)
        }
    }

    fun load() {
        scope.launch {
            loading = true
            errorMessage = null
            preferences = settingsRepository.readPreferences()
            when (val result = authRepository.currentUser()) {
                is ApiResult.Success -> {
                    user = result.value
                    displayName = result.value.displayName
                    timezone = result.value.timezone ?: "Asia/Manila"
                }
                is ApiResult.Failure -> errorMessage = result.error.userMessage()
            }
            loading = false
        }
    }

    LaunchedEffect(Unit) { load() }

    if (loading) {
        Text(
            text = "Loading settings",
            modifier = Modifier
                .fillMaxSize()
                .padding(contentPadding)
                .padding(24.dp),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        return
    }

    if (errorMessage != null || user == null) {
        CSNexusRetryPanel(
            title = "Could not load settings",
            body = errorMessage ?: "Settings were unavailable.",
            onRetry = ::load,
            modifier = Modifier.padding(contentPadding),
        )
        return
    }

    if (showDeleteDialog) {
        DeleteAccountDialog(
            authRepository = authRepository,
            onDismiss = { showDeleteDialog = false },
            onDeleted = onLoggedOut,
        )
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding)
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        // Back button is handled by the navigation scaffold's top bar.
        // GradientText h1 heading
        MetallicText(
            text = "Settings",
            style = MaterialTheme.typography.headlineLarge,
        )

        // Profile section
        GlassMedium(modifier = Modifier.fillMaxWidth()) {
            Column(
                modifier = Modifier.padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                SectionHeader("Profile", "Server owned")
                CSNexusTextField(
                    value = displayName,
                    onValueChange = {
                        displayName = it.take(255)
                        profileMessage = null
                    },
                    label = "Display name",
                )
                CSNexusTextField(
                    value = timezone,
                    onValueChange = {
                        timezone = it.take(80)
                        profileMessage = null
                    },
                    label = "Timezone",
                )
                Text(user?.email.orEmpty(), color = MaterialTheme.colorScheme.onSurfaceVariant)
                StatusMessage(profileMessage)
                CSNexusButton(
                    text = "Save profile",
                    onClick = {
                        val trimmedName = displayName.trim()
                        val trimmedTimezone = timezone.trim().ifBlank { "Asia/Manila" }
                        if (trimmedName.isEmpty()) {
                            profileMessage = "Display name is required."
                            return@CSNexusButton
                        }
                        scope.launch {
                            savingProfile = true
                            when (val result = authRepository.updateProfile(trimmedName, trimmedTimezone)) {
                                is ApiResult.Success -> {
                                    user = result.value
                                    displayName = result.value.displayName
                                    timezone = result.value.timezone ?: trimmedTimezone
                                    profileMessage = "Profile updated."
                                }
                                is ApiResult.Failure -> profileMessage = result.error.userMessage()
                            }
                            savingProfile = false
                        }
                    },
                    loading = savingProfile,
                    modifier = Modifier.fillMaxWidth(),
                )
            }
        }

        // Study Preferences section
        GlassMedium(modifier = Modifier.fillMaxWidth()) {
            Column(
                modifier = Modifier.padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                SectionHeader("Study Preferences", "Server + local")
                Text("Daily study goal: ${preferences.dailyGoalMinutes} minutes")
                Slider(
                    value = preferences.dailyGoalMinutes.toFloat(),
                    onValueChange = { value ->
                        val rounded = (value / 5f).roundToInt() * 5
                        if (isValidDailyGoalMinutes(rounded)) {
                            savePreferences(preferences.copy(dailyGoalMinutes = rounded))
                        }
                    },
                    valueRange = 5f..180f,
                    steps = 34,
                )
                CSNexusSegmentedControl(
                    options = listOf("Practice", "Exam", "Power"),
                    selectedIndex = quizModes.indexOf(preferences.defaultQuizMode).coerceAtLeast(0),
                    onSelected = { index ->
                        savePreferences(preferences.copy(defaultQuizMode = quizModes[index]))
                    },
                )
                CSNexusTextField(
                    value = preferences.examDate,
                    onValueChange = { savePreferences(preferences.copy(examDate = it.take(10))) },
                    label = "Exam date",
                    supportingText = "YYYY-MM-DD",
                )
                CSNexusTextField(
                    value = targetXp,
                    onValueChange = {
                        targetXp = it.filter(Char::isDigit).take(3)
                        targetMessage = null
                    },
                    label = "Daily XP target",
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                )
                if (syncBanner != null) {
                    CSNexusOfflineBanner(message = syncBanner!!.message)
                    CSNexusButton(
                        text = "Retry sync",
                        onClick = {
                            scope.launch {
                                when (val result = settingsRepository.retrySync()) {
                                    is ApiResult.Success -> {
                                        if (result.value > 0) targetMessage = "Retried queued settings changes."
                                    }
                                    is ApiResult.Failure -> targetMessage = result.error.userMessage()
                                }
                            }
                        },
                        variant = CSNexusButtonVariant.Ghost,
                        modifier = Modifier.fillMaxWidth(),
                    )
                }
                StatusMessage(targetMessage)
                CSNexusButton(
                    text = "Save XP target",
                    onClick = {
                        val nextTarget = targetXp.toIntOrNull()
                        if (nextTarget == null || !isValidDailyGoalXp(nextTarget)) {
                            targetMessage = "Daily XP target must be between 10 and 500."
                            return@CSNexusButton
                        }
                        scope.launch {
                            savingTarget = true
                            when (val result = settingsRepository.saveDailyGoal(nextTarget)) {
                                is ApiResult.Success -> {
                                    targetXp = (result.value.targetXp ?: nextTarget).toString()
                                    targetMessage = "Daily XP target saved."
                                }
                                is ApiResult.Failure -> targetMessage = result.error.userMessage()
                            }
                            savingTarget = false
                        }
                    },
                    loading = savingTarget,
                    variant = CSNexusButtonVariant.Secondary,
                    modifier = Modifier.fillMaxWidth(),
                )
            }
        }

        // Accessibility & Display section
        GlassMedium(modifier = Modifier.fillMaxWidth()) {
            Column(
                modifier = Modifier.padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                SectionHeader("Accessibility", "Local")
                PreferenceSegments(
                    label = "Reduced motion",
                    options = listOf("System", "On", "Off"),
                    values = listOf("system", "on", "off"),
                    selected = preferences.reducedMotion,
                    onSelected = { savePreferences(preferences.copy(reducedMotion = it)) },
                )
                PreferenceSegments(
                    label = "Font size",
                    options = listOf("Compact", "Default", "Large"),
                    values = listOf("compact", "default", "large"),
                    selected = preferences.fontSize,
                    onSelected = { savePreferences(preferences.copy(fontSize = it)) },
                )
                PreferenceSegments(
                    label = "Theme",
                    options = listOf("System", "Dark"),
                    values = listOf("system", "dark"),
                    selected = if (preferences.theme == "light") "dark" else preferences.theme,
                    onSelected = { savePreferences(preferences.copy(theme = it)) },
                )
                SettingToggle(
                    title = "Notifications",
                    body = "Device reminders and study nudges",
                    checked = preferences.notificationsEnabled,
                    onCheckedChange = { savePreferences(preferences.copy(notificationsEnabled = it)) },
                )
                SettingToggle(
                    title = "Sound",
                    body = "Audio feedback for learning actions",
                    checked = preferences.soundEnabled,
                    onCheckedChange = { savePreferences(preferences.copy(soundEnabled = it)) },
                )
                SettingToggle(
                    title = "Haptics",
                    body = "Vibration feedback for selections and results",
                    checked = preferences.hapticEnabled,
                    onCheckedChange = { savePreferences(preferences.copy(hapticEnabled = it)) },
                )
            }
        }

        // Account section
        GlassMedium(modifier = Modifier.fillMaxWidth()) {
            Column(
                modifier = Modifier.padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                SectionHeader("Account", "Server owned")
                CSNexusTextField(
                    value = currentPassword,
                    onValueChange = {
                        currentPassword = it
                        passwordMessage = null
                    },
                    label = "Current password",
                    visualTransformation = PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                )
                CSNexusTextField(
                    value = newPassword,
                    onValueChange = {
                        newPassword = it
                        passwordMessage = null
                    },
                    label = "New password",
                    visualTransformation = PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                    supportingText = "8+ chars, uppercase, lowercase, digit, symbol",
                )
                StatusMessage(passwordMessage)
                CSNexusButton(
                    text = "Change password",
                    onClick = {
                        if (currentPassword.isBlank()) {
                            passwordMessage = "Current password is required."
                            return@CSNexusButton
                        }
                        if (!isValidPassword(newPassword)) {
                            passwordMessage = "New password does not meet all policy requirements."
                            return@CSNexusButton
                        }
                        scope.launch {
                            changingPassword = true
                            when (val result = authRepository.changePassword(currentPassword, newPassword)) {
                                is ApiResult.Success -> {
                                    passwordMessage = "Password changed. Please log in again."
                                    currentPassword = ""
                                    newPassword = ""
                                    authRepository.clearLocalSession()
                                    onLoggedOut()
                                }
                                is ApiResult.Failure -> passwordMessage = result.error.userMessage()
                            }
                            changingPassword = false
                        }
                    },
                    loading = changingPassword,
                    modifier = Modifier.fillMaxWidth(),
                )
                CSNexusButton(
                    text = "Log out",
                    onClick = {
                        scope.launch {
                            authRepository.logout()
                            onLoggedOut()
                        }
                    },
                    variant = CSNexusButtonVariant.Secondary,
                    modifier = Modifier.fillMaxWidth(),
                )
                CSNexusButton(
                    text = "Delete account",
                    onClick = { showDeleteDialog = true },
                    variant = CSNexusButtonVariant.Danger,
                    modifier = Modifier.fillMaxWidth(),
                )
            }
        }
    }
}

@Composable
private fun SectionHeader(title: String, ownership: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        MetallicText(
            text = title,
            style = MaterialTheme.typography.titleLarge,
        )
        CSNexusStatusBadge(text = ownership)
    }
}

@Composable
private fun PreferenceSegments(
    label: String,
    options: List<String>,
    values: List<String>,
    selected: String,
    onSelected: (String) -> Unit,
) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Text(label, style = MaterialTheme.typography.titleMedium)
        CSNexusSegmentedControl(
            options = options,
            selectedIndex = values.indexOf(selected).coerceAtLeast(0),
            onSelected = { onSelected(values[it]) },
        )
    }
}

@Composable
private fun SettingToggle(
    title: String,
    body: String,
    checked: Boolean,
    onCheckedChange: (Boolean) -> Unit,
) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(16.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(title, style = MaterialTheme.typography.titleMedium)
            Text(body, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        Switch(
            checked = checked,
            onCheckedChange = onCheckedChange,
            colors = SwitchDefaults.colors(
                checkedThumbColor = Color.White,
                checkedTrackColor = GoldActive,
                checkedBorderColor = GoldActive,
                uncheckedThumbColor = MaterialTheme.colorScheme.onSurfaceVariant,
                uncheckedTrackColor = MaterialTheme.colorScheme.surfaceVariant,
                uncheckedBorderColor = MaterialTheme.colorScheme.outline,
            ),
        )
    }
}

@Composable
private fun StatusMessage(message: String?) {
    if (message != null) {
        Text(
            text = message,
            color = if (message.endsWith(".")) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error,
        )
    }
}

@Composable
private fun DeleteAccountDialog(
    authRepository: AuthRepository,
    onDismiss: () -> Unit,
    onDeleted: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    var phrase by remember { mutableStateOf("") }
    var deleting by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    val matches = phrase == DELETE_ACCOUNT_CONFIRMATION

    AlertDialog(
        onDismissRequest = {
            if (!deleting) onDismiss()
        },
        title = { Text("Delete account") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Text("This action is permanent and cannot be undone.")
                CSNexusTextField(
                    value = phrase,
                    onValueChange = {
                        phrase = it
                        error = null
                    },
                    label = DELETE_ACCOUNT_CONFIRMATION,
                    supportingText = "Type the confirmation phrase exactly.",
                )
                if (error != null) Text(error.orEmpty(), color = MaterialTheme.colorScheme.error)
            }
        },
        confirmButton = {
            CSNexusButton(
                text = "Delete",
                onClick = {
                    if (!matches) return@CSNexusButton
                    scope.launch {
                        deleting = true
                        when (val result = authRepository.deleteAccount(DELETE_ACCOUNT_CONFIRMATION)) {
                            is ApiResult.Success -> onDeleted()
                            is ApiResult.Failure -> {
                                error = result.error.userMessage()
                                deleting = false
                            }
                        }
                    }
                },
                enabled = matches,
                loading = deleting,
                variant = CSNexusButtonVariant.Danger,
            )
        },
        dismissButton = {
            CSNexusButton(
                text = "Cancel",
                onClick = onDismiss,
                enabled = !deleting,
                variant = CSNexusButtonVariant.Ghost,
            )
        },
    )
}

private val quizModes = listOf("practice", "exam", "power")
