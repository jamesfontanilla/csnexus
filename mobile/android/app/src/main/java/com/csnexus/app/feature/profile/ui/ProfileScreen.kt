package com.csnexus.app.feature.profile.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.auth.AuthRepository
import com.csnexus.app.core.design.AnimatedNumber
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.CSNexusRetryPanel
import com.csnexus.app.core.design.CSNexusStatusBadge
import com.csnexus.app.core.design.CSNexusTextField
import com.csnexus.app.core.design.GlassMedium
import com.csnexus.app.core.design.LuxuryProgressBar
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.design.PremiumCard
import com.csnexus.app.core.design.StaggeredItem
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.auth.data.UserDto
import com.csnexus.app.feature.progress.data.AchievementDto
import com.csnexus.app.feature.progress.data.ProgressRepository
import com.csnexus.app.feature.progress.data.XpDto
import kotlinx.coroutines.launch

@Composable
fun ProfileScreen(
    authRepository: AuthRepository,
    progressRepository: ProgressRepository,
    contentPadding: PaddingValues,
    onOpenSettings: () -> Unit,
    onLoggedOut: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    var user by remember { mutableStateOf<UserDto?>(null) }
    var xp by remember { mutableStateOf<XpDto?>(null) }
    var achievements by remember { mutableStateOf<List<AchievementDto>>(emptyList()) }
    var loading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }
    var editingName by remember { mutableStateOf(false) }
    var nameInput by remember { mutableStateOf("") }
    var savingName by remember { mutableStateOf(false) }
    var saveError by remember { mutableStateOf<String?>(null) }

    fun load() {
        scope.launch {
            loading = true
            errorMessage = null

            when (val result = authRepository.currentUser()) {
                is ApiResult.Success -> {
                    user = result.value
                    nameInput = result.value.displayName
                }
                is ApiResult.Failure -> {
                    errorMessage = result.error.userMessage()
                }
            }
            when (val result = progressRepository.xp()) {
                is ApiResult.Success -> xp = result.value
                is ApiResult.Failure -> Unit
            }
            when (val result = progressRepository.achievements()) {
                is ApiResult.Success -> achievements = result.value
                is ApiResult.Failure -> achievements = emptyList()
            }

            loading = false
        }
    }

    LaunchedEffect(Unit) { load() }

    if (loading) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(contentPadding),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
        ) {
            CircularProgressIndicator()
            Text(
                text = "Loading profile",
                modifier = Modifier.padding(top = 12.dp),
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
        return
    }

    if (errorMessage != null || user == null) {
        CSNexusRetryPanel(
            title = "Could not load profile",
            body = errorMessage ?: "Profile data was unavailable.",
            onRetry = ::load,
            modifier = Modifier.padding(contentPadding),
        )
        return
    }

    val profile = user ?: return
    val currentXp = xp
    val xpPerLevel = 100
    val xpInLevel = currentXp?.cumulativeXp?.rem(xpPerLevel) ?: 0

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding)
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        // Profile heading
        MetallicText(
            text = "Profile",
            style = MaterialTheme.typography.headlineLarge,
        )

        // Avatar + editable name + email
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Surface(
                modifier = Modifier.size(64.dp),
                shape = CircleShape,
                color = MaterialTheme.colorScheme.primaryContainer,
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center,
                ) {
                    Text(
                        text = profile.displayName.firstOrNull()?.uppercaseChar()?.toString() ?: "C",
                        style = MaterialTheme.typography.headlineMedium,
                        color = MaterialTheme.colorScheme.onPrimaryContainer,
                    )
                }
            }

            Column(modifier = Modifier.weight(1f)) {
                if (editingName) {
                    CSNexusTextField(
                        value = nameInput,
                        onValueChange = {
                            nameInput = it.take(255)
                            saveError = null
                        },
                        label = "Display name",
                    )
                } else {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = profile.displayName,
                            modifier = Modifier.weight(1f),
                            style = MaterialTheme.typography.headlineSmall,
                            fontWeight = FontWeight.SemiBold,
                        )
                        IconButton(onClick = { editingName = true }) {
                            Icon(Icons.Filled.Edit, contentDescription = "Edit display name")
                        }
                    }
                }
                Text(profile.email, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text(profile.category, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }

        // Save/Cancel buttons when editing
        if (editingName) {
            if (saveError != null) {
                Text(saveError.orEmpty(), color = MaterialTheme.colorScheme.error)
            }
            Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                CSNexusButton(
                    text = "Save",
                    onClick = {
                        val trimmed = nameInput.trim()
                        if (trimmed.isEmpty()) {
                            saveError = "Display name is required."
                            return@CSNexusButton
                        }
                        if (trimmed == profile.displayName) {
                            editingName = false
                            return@CSNexusButton
                        }
                        scope.launch {
                            savingName = true
                            when (val result = authRepository.updateDisplayName(trimmed)) {
                                is ApiResult.Success -> {
                                    user = result.value
                                    nameInput = result.value.displayName
                                    editingName = false
                                }
                                is ApiResult.Failure -> saveError = result.error.userMessage()
                            }
                            savingName = false
                        }
                    },
                    loading = savingName,
                    modifier = Modifier.weight(1f),
                )
                CSNexusButton(
                    text = "Cancel",
                    onClick = {
                        nameInput = profile.displayName
                        saveError = null
                        editingName = false
                    },
                    variant = CSNexusButtonVariant.Secondary,
                    enabled = !savingName,
                    modifier = Modifier.weight(1f),
                )
            }
        }

        // Progress card with 3-column grid + LuxuryProgressBar
        GlassMedium(modifier = Modifier.fillMaxWidth()) {
            Column(
                modifier = Modifier.padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
            ) {
                MetallicText("Progress", style = MaterialTheme.typography.titleLarge)
                if (currentXp == null) {
                    Text(
                        "Progress data is unavailable.",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                } else {
                    // 3-column stat grid: Level | Total XP | Streak
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                    ) {
                        // Level as MetallicText
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            MetallicText(
                                text = currentXp.level.toString(),
                                style = MaterialTheme.typography.headlineSmall,
                            )
                            Text(
                                "Level",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                style = MaterialTheme.typography.labelMedium,
                            )
                        }
                        // Total XP with AnimatedNumber
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            AnimatedNumber(
                                target = currentXp.cumulativeXp,
                                style = MaterialTheme.typography.headlineSmall,
                                durationMs = 1000,
                            )
                            Text(
                                "Total XP",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                style = MaterialTheme.typography.labelMedium,
                            )
                        }
                        // Streak with 🔥 + AnimatedNumber
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text("🔥", style = MaterialTheme.typography.headlineSmall)
                                AnimatedNumber(
                                    target = currentXp.streak,
                                    style = MaterialTheme.typography.headlineSmall,
                                    durationMs = 1000,
                                )
                            }
                            Text(
                                "Streak",
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                style = MaterialTheme.typography.labelMedium,
                            )
                        }
                    }

                    // LuxuryProgressBar for XP to next level
                    LuxuryProgressBar(
                        progress = xpInLevel / xpPerLevel.toFloat(),
                        modifier = Modifier.fillMaxWidth(),
                    )
                    Text(
                        text = "$xpInLevel XP to Level ${currentXp.level + 1}",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        style = MaterialTheme.typography.bodySmall,
                    )
                }
            }
        }

        // Achievements section — staggered GlassMedium cards
        MetallicText("Achievements", style = MaterialTheme.typography.titleLarge)
        if (achievements.isEmpty()) {
            Text(
                "No achievements yet. Keep learning!",
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        } else {
            achievements.forEachIndexed { index, achievement ->
                StaggeredItem(index = index) {
                    GlassMedium(modifier = Modifier.fillMaxWidth()) {
                        Row(
                            modifier = Modifier.padding(16.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(12.dp),
                        ) {
                            Text("🏅", style = MaterialTheme.typography.headlineSmall)
                            Column(modifier = Modifier.weight(1f)) {
                                Text(
                                    achievement.title,
                                    style = MaterialTheme.typography.titleMedium,
                                    fontWeight = FontWeight.SemiBold,
                                )
                                if (achievement.description.isNotBlank()) {
                                    Text(
                                        achievement.description,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    )
                                }
                            }
                            if (achievement.grantedAt.isNotBlank()) {
                                CSNexusStatusBadge(text = achievement.grantedAt.take(10))
                            }
                        }
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        // Settings link as PremiumCard
        PremiumCard(onClick = onOpenSettings) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(20.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Column {
                    Text(
                        "Settings",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                    )
                    Text(
                        "Preferences, accessibility, and account",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        style = MaterialTheme.typography.bodySmall,
                    )
                }
                Icon(
                    Icons.Filled.ChevronRight,
                    contentDescription = "Open settings",
                    tint = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }

        // Log out button
        CSNexusButton(
            text = "Log out",
            onClick = {
                scope.launch {
                    authRepository.logout()
                    onLoggedOut()
                }
            },
            variant = CSNexusButtonVariant.Danger,
            modifier = Modifier.fillMaxWidth(),
        )
    }
}
