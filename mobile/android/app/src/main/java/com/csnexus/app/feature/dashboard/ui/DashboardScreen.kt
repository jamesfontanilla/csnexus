package com.csnexus.app.feature.dashboard.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.design.AnimatedNumber
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.LuxuryDivider
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.design.PremiumCard
import com.csnexus.app.core.design.ProgressRing
import com.csnexus.app.core.design.shadowGlow

@Composable
fun DashboardScreen(
    contentPadding: PaddingValues,
    onOpenModules: () -> Unit,
    onOpenQuiz: () -> Unit,
    onOpenMockExam: () -> Unit,
    onOpenFlashcards: () -> Unit,
    onOpenLeaderboards: () -> Unit,
    onOpenProgress: () -> Unit,
    onOpenFocus: () -> Unit,
    onOpenQueue: () -> Unit,
    onOpenMilestones: () -> Unit,
    onOpenOnboarding: () -> Unit,
    onOpenTutor: () -> Unit,
    onOpenRelease: () -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding)
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        // Hero section: premium card with metallic header + progress ring
        PremiumCard {
            Column(
                verticalArrangement = Arrangement.spacedBy(12.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                modifier = Modifier.fillMaxWidth().padding(16.dp),
            ) {
                MetallicText("Dashboard")
                Box(
                    modifier = Modifier.size(160.dp),
                    contentAlignment = Alignment.Center,
                ) {
                    ProgressRing(
                        value = 75,
                        ringSize = 160.dp,
                        label = "Readiness",
                    )
                    Text(
                        text = "75%",
                        style = MaterialTheme.typography.headlineMedium,
                        color = MaterialTheme.colorScheme.onSurface,
                    )
                }
                Text(
                    "Your native CSNexus app foundation is running. Next milestone work will wire progress, recommendations, and study streak data from the API.",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                CSNexusButton(
                    text = "Open Modules",
                    onClick = onOpenModules,
                    modifier = Modifier.fillMaxWidth(),
                )
            }
        }

        // Stat cards with animated numbers + gold glow
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            PremiumCard(modifier = Modifier.weight(1f).shadowGlow()) {
                Column(
                    verticalArrangement = Arrangement.spacedBy(6.dp),
                    modifier = Modifier.padding(12.dp),
                ) {
                    Text("Practice", style = MaterialTheme.typography.titleMedium)
                    AnimatedNumber(
                        target = 42,
                        durationMs = 1000,
                        style = MaterialTheme.typography.headlineSmall,
                        suffix = " sessions",
                    )
                    Text(
                        "Quiz, mock exam, flashcards, and tutor.",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
            PremiumCard(modifier = Modifier.weight(1f).shadowGlow()) {
                Column(
                    verticalArrangement = Arrangement.spacedBy(6.dp),
                    modifier = Modifier.padding(12.dp),
                ) {
                    Text("Tracking", style = MaterialTheme.typography.titleMedium)
                    AnimatedNumber(
                        target = 87,
                        durationMs = 1200,
                        style = MaterialTheme.typography.headlineSmall,
                        suffix = "%",
                    )
                    Text(
                        "Progress, goals, and readiness surfaces.",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }

        // Luxury divider between hero/stats section and quick action buttons
        LuxuryDivider()

        // Quick action button grid (unchanged navigation callbacks)
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            CSNexusButton(text = "Quiz", onClick = onOpenQuiz, variant = CSNexusButtonVariant.Secondary, modifier = Modifier.weight(1f))
            CSNexusButton(text = "Mock Exam", onClick = onOpenMockExam, variant = CSNexusButtonVariant.Secondary, modifier = Modifier.weight(1f))
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            CSNexusButton(text = "Flashcards", onClick = onOpenFlashcards, variant = CSNexusButtonVariant.Secondary, modifier = Modifier.weight(1f))
            CSNexusButton(text = "Progress", onClick = onOpenProgress, variant = CSNexusButtonVariant.Secondary, modifier = Modifier.weight(1f))
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            CSNexusButton(text = "Leaderboards", onClick = onOpenLeaderboards, variant = CSNexusButtonVariant.Secondary, modifier = Modifier.weight(1f))
            CSNexusButton(text = "Focus", onClick = onOpenFocus, variant = CSNexusButtonVariant.Secondary, modifier = Modifier.weight(1f))
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            CSNexusButton(text = "Queue", onClick = onOpenQueue, variant = CSNexusButtonVariant.Secondary, modifier = Modifier.weight(1f))
            CSNexusButton(text = "Milestones", onClick = onOpenMilestones, variant = CSNexusButtonVariant.Secondary, modifier = Modifier.weight(1f))
        }
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            CSNexusButton(text = "Onboarding", onClick = onOpenOnboarding, variant = CSNexusButtonVariant.Secondary, modifier = Modifier.weight(1f))
            CSNexusButton(text = "Tutor", onClick = onOpenTutor, variant = CSNexusButtonVariant.Secondary, modifier = Modifier.weight(1f))
        }
        CSNexusButton(
            text = "Release Readiness",
            onClick = onOpenRelease,
            variant = CSNexusButtonVariant.Ghost,
            modifier = Modifier.fillMaxWidth(),
        )
    }
}
