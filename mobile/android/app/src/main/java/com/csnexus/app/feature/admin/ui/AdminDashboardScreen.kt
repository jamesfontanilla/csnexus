package com.csnexus.app.feature.admin.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.PremiumCard
import com.csnexus.app.core.design.CSNexusConfirmDialog
import com.csnexus.app.core.design.CSNexusRetryPanel
import com.csnexus.app.core.design.CSNexusSearchField
import com.csnexus.app.core.design.CSNexusSkeleton
import com.csnexus.app.core.design.CSNexusStatusBadge
import com.csnexus.app.core.design.GlassToast
import com.csnexus.app.core.design.GlassToastState
import com.csnexus.app.core.design.GlassToastVariant
import com.csnexus.app.core.design.LuxuryProgressBar
import com.csnexus.app.core.design.csnexusHeading
import com.csnexus.app.feature.admin.data.AdminAnalyticsDto
import com.csnexus.app.feature.admin.data.AdminRepositoryContract
import com.csnexus.app.feature.admin.data.AdminUserDto
import kotlin.math.roundToInt

@Composable
fun AdminDashboardScreen(
    contentPadding: PaddingValues,
    isAdmin: Boolean,
    adminRepository: AdminRepositoryContract,
    viewModel: AdminViewModel = viewModel(factory = AdminViewModelFactory(adminRepository, isAdmin)),
) {
    // ── Defense-in-depth role gate ────────────────────────────────────────────
    if (!isAdmin) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(contentPadding)
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
        ) {
            Icon(
                imageVector = Icons.Filled.Lock,
                contentDescription = null,
                modifier = Modifier.size(48.dp),
                tint = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text(
                text = "Admin access required",
                modifier = Modifier.padding(top = 16.dp),
                style = MaterialTheme.typography.headlineMedium,
            )
            Text(
                text = "This area is restricted to admin accounts. Your current account does not have admin permissions.",
                modifier = Modifier.padding(top = 8.dp),
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
        return
    }

    val state by viewModel.uiState.collectAsState()
    var toastState by remember { mutableStateOf<GlassToastState?>(null) }

    // Show action feedback with the shared glass toast surface.
    LaunchedEffect(state.actionMessage) {
        state.actionMessage?.let { msg ->
            toastState = GlassToastState(
                message = msg,
                variant = GlassToastVariant.Info,
            )
            viewModel.clearActionMessage()
        }
    }

    // Confirm delete dialog
    state.deleteTarget?.let { target ->
        CSNexusConfirmDialog(
            title = "Delete user?",
            body = "This will permanently delete ${target.email}. This cannot be undone.",
            confirmText = "Delete",
            onConfirm = { viewModel.confirmDelete() },
            onDismiss = { viewModel.dismissDelete() },
            danger = true,
        )
    }

    Box(modifier = Modifier.fillMaxSize()) {
        LazyColumn(
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(
                start = 20.dp,
                end = 20.dp,
                top = contentPadding.calculateTopPadding() + 8.dp,
                bottom = contentPadding.calculateBottomPadding() + 20.dp,
            ),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            // ── Header ────────────────────────────────────────────────────────
            item {
                Text(
                    text = "Admin Dashboard",
                    modifier = Modifier.csnexusHeading(),
                    style = MaterialTheme.typography.headlineMedium,
                )
                Text(
                    "Platform analytics and user management.",
                    modifier = Modifier.padding(top = 4.dp),
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }

            // ── Analytics section ─────────────────────────────────────────────
            item {
                Text("Analytics", style = MaterialTheme.typography.titleLarge)
            }

            if (state.analyticsLoading) {
                items(3) {
                    CSNexusSkeleton(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(72.dp),
                    )
                }
            } else if (state.analytics == null && !state.usersLoading) {
                item {
                    CSNexusRetryPanel(
                        title = "Analytics unavailable",
                        body = state.errorMessage ?: "Could not load analytics.",
                        onRetry = { viewModel.load() },
                    )
                }
            } else if (state.analytics != null) {
                item {
                    AnalyticsSection(analytics = state.analytics!!)
                }
            }

            // ── User management section ───────────────────────────────────────
            item {
                Spacer(modifier = Modifier.height(4.dp))
                Text("User Management", style = MaterialTheme.typography.titleLarge)
            }

            item {
                CSNexusSearchField(
                    value = state.searchQuery,
                    onValueChange = viewModel::onSearchChanged,
                    placeholder = "Search by email, name, or username",
                )
            }

            if (state.usersLoading) {
                items(4) {
                    CSNexusSkeleton(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(96.dp),
                    )
                }
            } else if (state.filteredUsers.isEmpty() && state.searchQuery.isBlank()) {
                item {
                    PremiumCard {
                        Text(
                            "No users found.",
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
            } else if (state.filteredUsers.isEmpty()) {
                item {
                    PremiumCard {
                        Text(
                            "No users match \"${state.searchQuery}\".",
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
            } else {
                items(state.filteredUsers, key = { it.id }) { user ->
                    AdminUserRow(
                        user = user,
                        onToggleBan = { viewModel.toggleBan(user) },
                        onDelete = { viewModel.requestDelete(user) },
                        isDeleting = state.isDeleting && state.deleteTarget?.id == user.id,
                    )
                }
            }

            // ── Error banner ──────────────────────────────────────────────────
            if (state.errorMessage != null && !state.analyticsLoading && !state.usersLoading) {
                item {
                    CSNexusRetryPanel(
                        title = "Something went wrong",
                        body = state.errorMessage!!,
                        onRetry = { viewModel.load() },
                    )
                }
            }
        }

        GlassToast(
            state = toastState,
            onDismiss = { toastState = null },
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(top = contentPadding.calculateTopPadding() + 12.dp, end = 12.dp),
        )
    }
}

// ── Analytics section ─────────────────────────────────────────────────────────

@Composable
private fun AnalyticsSection(analytics: AdminAnalyticsDto) {
    val passRatePct = (analytics.mockPassRate * 100).roundToInt()

    // Accessible platform summary for screen readers
    Text(
        text = "Platform summary: ${analytics.totalUsers} total users, " +
            "${analytics.verifiedUsers} verified, ${analytics.bannedUsers} banned.",
        modifier = Modifier
            .fillMaxWidth()
            .semantics { liveRegion = LiveRegionMode.Polite },
        style = MaterialTheme.typography.bodySmall,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
    )

    Spacer(modifier = Modifier.height(8.dp))

    // 2-column metric grid
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            MetricCard(
                modifier = Modifier.weight(1f),
                label = "Total Users",
                value = analytics.totalUsers.toString(),
            )
            MetricCard(
                modifier = Modifier.weight(1f),
                label = "Verified",
                value = analytics.verifiedUsers.toString(),
            )
        }
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            MetricCard(
                modifier = Modifier.weight(1f),
                label = "Banned",
                value = analytics.bannedUsers.toString(),
            )
            MetricCard(
                modifier = Modifier.weight(1f),
                label = "Lessons Done",
                value = analytics.totalLessonsCompleted.toString(),
            )
        }
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            MetricCard(
                modifier = Modifier.weight(1f),
                label = "Quiz Attempts",
                value = analytics.totalQuizAttempts.toString(),
            )
            MetricCard(
                modifier = Modifier.weight(1f),
                label = "Mock Attempts",
                value = analytics.totalMockAttempts.toString(),
            )
        }
        MetricCard(
            label = "Mock Pass Rate",
            value = "$passRatePct%",
        )
    }

    // Weakest subtopics
    if (analytics.weakestSubtopics.isNotEmpty()) {
        Spacer(modifier = Modifier.height(12.dp))
        Text("Weakest Subtopics", style = MaterialTheme.typography.titleMedium)
        Spacer(modifier = Modifier.height(8.dp))
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            analytics.weakestSubtopics.forEach { subtopic ->
                val score = (subtopic.avgScore * 100).roundToInt().coerceIn(0, 100)
                PremiumCard {
                    Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                        ) {
                            Text(subtopic.title, style = MaterialTheme.typography.bodyMedium)
                            Text(
                                "$score%",
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                        LuxuryProgressBar(
                            progress = score / 100f,
                            modifier = Modifier
                                .fillMaxWidth()
                                .semantics {
                                    liveRegion = LiveRegionMode.Polite
                                },
                        )
                        // Accessible label for screen readers
                        Text(
                            text = "${subtopic.title}: average score $score%",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun MetricCard(
    label: String,
    value: String,
    modifier: Modifier = Modifier,
) {
    PremiumCard(modifier = modifier) {
        Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(
                text = label,
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text(
                text = value,
                modifier = Modifier.semantics { liveRegion = LiveRegionMode.Polite },
                style = MaterialTheme.typography.headlineMedium,
            )
        }
    }
}

// ── User row ──────────────────────────────────────────────────────────────────

@Composable
private fun AdminUserRow(
    user: AdminUserDto,
    onToggleBan: () -> Unit,
    onDelete: () -> Unit,
    isDeleting: Boolean,
) {
    val authMethod = if (user.googleId != null) "Google" else "Email"
    val banLabel = if (user.isBanned) "Unban" else "Ban"

    PremiumCard {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            // User identifiers
            Text(user.email, style = MaterialTheme.typography.titleMedium)
            Text(
                text = "${user.displayName} · ${user.username ?: "—"} · $authMethod",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            // Badges
            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                CSNexusStatusBadge(
                    text = user.role.lowercase().replaceFirstChar { it.uppercase() },
                    color = if (user.role.equals("admin", ignoreCase = true)) {
                        MaterialTheme.colorScheme.primary
                    } else {
                        MaterialTheme.colorScheme.secondary
                    },
                )
                if (user.isBanned) {
                    CSNexusStatusBadge(
                        text = "Banned",
                        color = MaterialTheme.colorScheme.error,
                    )
                }
                user.accountState?.let { state ->
                    if (state.isNotBlank()) {
                        CSNexusStatusBadge(
                            text = state.lowercase().replaceFirstChar { it.uppercase() },
                        )
                    }
                }
            }

            // Actions
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                CSNexusButton(
                    text = banLabel,
                    onClick = onToggleBan,
                    variant = if (user.isBanned) CSNexusButtonVariant.Secondary else CSNexusButtonVariant.Danger,
                    modifier = Modifier.weight(1f),
                )
                CSNexusButton(
                    text = "Delete",
                    onClick = onDelete,
                    variant = CSNexusButtonVariant.Danger,
                    modifier = Modifier.weight(1f),
                    loading = isDeleting,
                )
            }
        }

    }
}
