package com.csnexus.app.feature.motivation.ui

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
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
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.design.AnimatedNumber
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.CSNexusChip
import com.csnexus.app.core.design.CSNexusSkeleton
import com.csnexus.app.core.design.CSNexusStatusBadge
import com.csnexus.app.core.design.GlassMedium
import com.csnexus.app.core.design.LuxuryProgressBar
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.design.StaggeredItem
import com.csnexus.app.core.design.CSNexusMotion
import com.csnexus.app.core.design.rememberCSNexusReducedMotion
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.motivation.data.ConsistencyDto
import com.csnexus.app.feature.motivation.data.MilestoneStatusDto
import com.csnexus.app.feature.motivation.data.MotivationRepository
import com.csnexus.app.feature.progress.data.AchievementDto
import com.csnexus.app.feature.progress.data.ProgressRepository
import kotlinx.coroutines.launch

@Composable
fun MilestonesScreen(
    repository: MotivationRepository,
    progressRepository: ProgressRepository,
    contentPadding: PaddingValues,
) {
    val scope = rememberCoroutineScope()
    var milestones by remember { mutableStateOf<List<MilestoneStatusDto>>(emptyList()) }
    var consistency by remember { mutableStateOf<ConsistencyDto?>(null) }
    var achievements by remember { mutableStateOf<List<AchievementDto>>(emptyList()) }
    var loading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }

    fun loadAll() {
        loading = true
        errorMessage = null
        scope.launch {
            when (val result = repository.milestones()) {
                is ApiResult.Success -> milestones = result.value.milestones
                is ApiResult.Failure -> errorMessage = result.error.userMessage()
            }
            when (val result = repository.consistency()) {
                is ApiResult.Success -> consistency = result.value
                is ApiResult.Failure -> if (errorMessage == null) errorMessage = result.error.userMessage()
            }
            when (val result = progressRepository.achievements()) {
                is ApiResult.Success -> achievements = result.value
                is ApiResult.Failure -> Unit
            }
            loading = false
        }
    }

    LaunchedEffect(Unit) {
        loadAll()
    }

    if (loading) {
        // Skeleton: circle + 4 cards
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(contentPadding)
                .padding(20.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            CSNexusSkeleton(modifier = Modifier.size(64.dp).clip(CircleShape))
            repeat(4) { CSNexusSkeleton(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp).run { this.then(Modifier) }) }
        }
        return
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding)
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        MetallicText("Milestones", style = MaterialTheme.typography.headlineMedium)
        if (errorMessage != null && milestones.isEmpty()) {
            MilestoneErrorCard(message = errorMessage!!, onRetry = ::loadAll)
            return@Column
        }
        if (errorMessage != null) {
            MilestoneErrorCard(message = errorMessage!!, onRetry = ::loadAll)
        }

        consistency?.let { metric ->
            GlassMedium(modifier = Modifier.fillMaxWidth()) {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    MetallicText("Study Consistency", style = MaterialTheme.typography.titleMedium)
                    Row(horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                        ConsistencyStat("Current streak", metric.currentStreak, Modifier.weight(1f))
                        ConsistencyStat("Longest streak", metric.longestStreak, Modifier.weight(1f))
                        ConsistencyStat("Total days", metric.totalConsistentDays, Modifier.weight(1f))
                    }
                    Text(
                        "Last qualifying day: ${formatFriendlyDate(metric.lastQualifyingDate)}",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }

        if (achievements.isNotEmpty()) {
            GlassMedium(modifier = Modifier.fillMaxWidth()) {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    MetallicText("Achievements", style = MaterialTheme.typography.titleMedium)
                    achievements.take(5).forEachIndexed { index, achievement ->
                        StaggeredItem(index = index) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                            ) {
                                Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
                                    Text("🏅 ${achievement.title}", fontWeight = FontWeight.SemiBold)
                                    if (achievement.description.isNotBlank()) {
                                        Text(achievement.description, color = MaterialTheme.colorScheme.onSurfaceVariant)
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
        }

        val grouped = groupMilestones(milestones)
        if (grouped.isEmpty()) {
            GlassMedium(modifier = Modifier.fillMaxWidth()) {
                Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("No milestones yet", style = MaterialTheme.typography.titleMedium)
                    Text("Milestones will appear as your progress begins to stick.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        } else {
            grouped.forEach { (category, items) ->
                Text(milestoneCategoryLabel(category), style = MaterialTheme.typography.titleLarge)
                items.forEachIndexed { index, milestone ->
                    StaggeredItem(index = index) {
                        MilestoneCard(milestone = milestone)
                    }
                }
            }
        }
    }
}

@Composable
private fun MilestoneCard(milestone: MilestoneStatusDto) {
    val isEarned = milestone.status == "earned"
    val isLocked = milestone.status == "locked"
    val reducedMotion = rememberCSNexusReducedMotion()
    val scale by animateFloatAsState(
        targetValue = if (isEarned) 1.02f else 1f,
        animationSpec = if (reducedMotion) CSNexusMotion.instant() else CSNexusMotion.springGentle(),
        label = "milestoneScale",
    )
    val iconColor = when {
        isEarned -> Color(0xFF4CAF50) // green border
        isLocked -> MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.4f)
        else -> Color(0xFFC9A84C) // gold for in-progress
    }
    GlassMedium(
        modifier = Modifier.fillMaxWidth().scale(scale),
    ) {
        Row(
            modifier = Modifier.padding(16.dp).fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            // 40dp circular icon
            androidx.compose.foundation.Canvas(
                modifier = Modifier.size(40.dp),
            ) {
                val radius = size.minDimension / 2f
                drawCircle(color = iconColor.copy(alpha = 0.15f), radius = radius)
                drawCircle(color = iconColor, radius = radius, style = androidx.compose.ui.graphics.drawscope.Stroke(width = 2.dp.toPx()))
            }
            Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                ) {
                    Text(milestone.name, style = MaterialTheme.typography.titleMedium, modifier = Modifier.weight(1f))
                    Text(
                        when (milestone.status) {
                            "earned" -> "✨"
                            "in_progress" -> "⏳"
                            else -> "🔒"
                        },
                    )
                }
                Text(milestone.description, color = MaterialTheme.colorScheme.onSurfaceVariant)
                if (milestone.status == "in_progress") {
                    LuxuryProgressBar(
                        progress = (milestone.progressPercentage / 100.0).toFloat().coerceIn(0f, 1f),
                        modifier = Modifier.fillMaxWidth(),
                    )
                }
                if (isEarned) {
                    CSNexusStatusBadge(text = formatFriendlyDate(milestone.awardedAt), color = Color(0xFF4CAF50))
                }
            }
        }
    }
}

@Composable
private fun ConsistencyStat(
    label: String,
    value: Int,
    modifier: Modifier = Modifier,
) {
    Column(modifier = modifier, verticalArrangement = Arrangement.spacedBy(4.dp), horizontalAlignment = Alignment.CenterHorizontally) {
        AnimatedNumber(target = value, style = MaterialTheme.typography.headlineSmall.copy(fontWeight = FontWeight.SemiBold))
        Text(label, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodySmall)
    }
}

@Composable
private fun MilestoneErrorCard(
    message: String,
    onRetry: () -> Unit,
) {
    GlassMedium(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("Could not load milestones", style = MaterialTheme.typography.titleMedium)
            Text(message, color = MaterialTheme.colorScheme.onSurfaceVariant)
            CSNexusButton(text = "Retry", onClick = onRetry, variant = CSNexusButtonVariant.Secondary)
        }
    }
}
