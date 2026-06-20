package com.csnexus.app.feature.home.ui

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
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.design.PremiumCard
import com.csnexus.app.core.design.StaggeredItem

private data class FeatureItem(
    val emoji: String,
    val title: String,
    val description: String,
)

private val features = listOf(
    FeatureItem(
        emoji = "📚",
        title = "Structured Lessons",
        description = "Modules, topics, subtopics, and segmented lesson reading.",
    ),
    FeatureItem(
        emoji = "⏱️",
        title = "Timed Practice",
        description = "Scoped quizzes, mock exams, flashcard study, and retry flows.",
    ),
    FeatureItem(
        emoji = "📊",
        title = "Visible Progress",
        description = "XP, mastery, readiness, goals, focus sessions, and milestones.",
    ),
    FeatureItem(
        emoji = "🏆",
        title = "Community",
        description = "Leaderboards, tournaments, flashcard marketplace, and tutor support.",
    ),
    FeatureItem(
        emoji = "🧠",
        title = "AI Tutor",
        description = "Step-by-step explanations, hints, and similar question generation.",
    ),
    FeatureItem(
        emoji = "🎯",
        title = "Exam Readiness",
        description = "Confidence scoring, predicted scores, and personalized study plans.",
    ),
)

@Composable
fun PublicHomeScreen(
    contentPadding: PaddingValues,
    isAuthenticated: Boolean,
    onContinueStudying: () -> Unit,
    onSignup: () -> Unit,
    onLogin: () -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding)
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        // Hero section
        HeroSection(
            isAuthenticated = isAuthenticated,
            onContinueStudying = onContinueStudying,
            onSignup = onSignup,
            onLogin = onLogin,
        )

        // Features grid
        FeaturesGrid()
    }
}

@Composable
private fun HeroSection(
    isAuthenticated: Boolean,
    onContinueStudying: () -> Unit,
    onSignup: () -> Unit,
    onLogin: () -> Unit,
) {
    Column(
        modifier = Modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(12.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        MetallicText(
            text = "CSNexus",
            style = MaterialTheme.typography.displayLarge,
        )

        Text(
            text = "Your free study companion for the Philippine Civil Service Examination.",
            style = MaterialTheme.typography.titleMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center,
        )

        Text(
            text = "Practice lessons, quizzes, mock exams, flashcards, and progress tracking in a native Android app.",
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            textAlign = TextAlign.Center,
        )

        Spacer(modifier = Modifier.height(8.dp))

        if (isAuthenticated) {
            CSNexusButton(
                text = "Continue studying",
                onClick = onContinueStudying,
                modifier = Modifier.fillMaxWidth(),
            )
        } else {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                CSNexusButton(
                    text = "Get started",
                    onClick = onSignup,
                    modifier = Modifier.weight(1f),
                )
                CSNexusButton(
                    text = "Log in",
                    onClick = onLogin,
                    variant = CSNexusButtonVariant.Secondary,
                    modifier = Modifier.weight(1f),
                )
            }
        }
    }
}

@Composable
private fun FeaturesGrid() {
    Column(
        modifier = Modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        // Render as rows of 3 (adaptive grid) using manual row layout
        // to avoid nested scrollable LazyVerticalGrid inside a scrollable Column.
        features.chunked(3).forEachIndexed { rowIndex, rowItems ->
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                rowItems.forEachIndexed { colIndex, feature ->
                    val index = rowIndex * 3 + colIndex
                    Box(modifier = Modifier.weight(1f)) {
                        StaggeredItem(index = index) {
                            FeatureCard(feature = feature)
                        }
                    }
                }
                // Fill remaining space if row has fewer than 3 items
                repeat(3 - rowItems.size) {
                    Spacer(modifier = Modifier.weight(1f))
                }
            }
        }
    }
}

@Composable
private fun FeatureCard(feature: FeatureItem) {
    PremiumCard(
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Text(
                text = feature.emoji,
                style = MaterialTheme.typography.headlineMedium,
            )
            Text(
                text = feature.title,
                style = MaterialTheme.typography.titleMedium,
            )
            Text(
                text = feature.description,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}
