package com.csnexus.app.feature.flashcards.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.design.CSNexusCard
import com.csnexus.app.core.design.CSNexusChip
import com.csnexus.app.core.design.LuxuryProgressBar
import com.csnexus.app.core.design.LoadingState
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.flashcards.data.AnalyticsDashboardDto
import com.csnexus.app.feature.flashcards.data.FlashcardRecommendationDto
import com.csnexus.app.feature.flashcards.data.FlashcardRepository
import com.csnexus.app.feature.flashcards.data.HeatmapEntryDto

@Composable
fun FlashcardAnalyticsScreen(
    repository: FlashcardRepository,
    contentPadding: PaddingValues,
) {
    var dashboard by remember { mutableStateOf<AnalyticsDashboardDto?>(null) }
    var recommendations by remember { mutableStateOf<List<FlashcardRecommendationDto>>(emptyList()) }
    var heatmap by remember { mutableStateOf<List<HeatmapEntryDto>>(emptyList()) }
    var loading by remember { mutableStateOf(true) }
    var errorMessage by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(Unit) {
        loading = true
        when (val dash = repository.analyticsDashboard()) {
            is ApiResult.Success -> dashboard = dash.value
            is ApiResult.Failure -> errorMessage = "Could not load flashcard analytics."
        }
        when (val recs = repository.recommendations()) {
            is ApiResult.Success -> recommendations = recs.value
            is ApiResult.Failure -> Unit
        }
        when (val heat = repository.heatmap()) {
            is ApiResult.Success -> heatmap = heat.value
            is ApiResult.Failure -> Unit
        }
        loading = false
    }

    if (loading) {
        LoadingState(label = "Loading flashcard analytics")
        return
    }

    val analytics = dashboard
    if (analytics == null) {
        Text(errorMessage ?: "No analytics available.", modifier = Modifier.padding(24.dp))
        return
    }

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            Text("Flashcard Analytics", style = MaterialTheme.typography.headlineMedium)
            Text(
                "Accessible summaries mirror the web dashboard without hiding the numbers inside decoration.",
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
        item {
            CSNexusCard(modifier = Modifier.heightIn(min = 148.dp)) {
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Text("Overall Retention", style = MaterialTheme.typography.titleMedium)
                    Text("${analytics.overallRetention.toInt()}%", style = MaterialTheme.typography.headlineLarge)
                    Text(
                        "${analytics.totalCardsStudied} cards studied across ${analytics.totalSessions} sessions",
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }
        item {
            ReadinessCard(readiness = analytics.predictedReadiness)
        }
        item {
            BreakdownCard(
                title = "Strongest Subjects",
                items = analytics.strongestSubjects.map { Triple(it.category, it.retentionRate, it.cardsStudied) },
            )
        }
        item {
            BreakdownCard(
                title = "Weakest Subjects",
                items = analytics.weakestSubjects.map { Triple(it.category, it.retentionRate, it.cardsStudied) },
            )
        }
        if (heatmap.isNotEmpty()) {
            item {
                HeatmapCard(heatmap = heatmap)
            }
        }
        if (recommendations.isNotEmpty()) {
            item {
                Text("Recommendations", style = MaterialTheme.typography.titleLarge)
            }
            items(recommendations, key = { it.id }) { recommendation ->
                CSNexusCard {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(recommendation.deckTitle, style = MaterialTheme.typography.titleMedium)
                        Text(recommendation.reason, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        RowWrap {
                            CSNexusChip(text = "Priority ${recommendation.priority}")
                            CSNexusChip(text = "Deck #${recommendation.deckId}")
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun ReadinessCard(readiness: Double) {
    val pct = readiness.coerceIn(0.0, 100.0)
    CSNexusCard(modifier = Modifier.heightIn(min = 140.dp)) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("Predicted Exam Readiness", style = MaterialTheme.typography.titleMedium)
            Text("${pct.toInt()}%", style = MaterialTheme.typography.headlineLarge)
            LuxuryProgressBar(
                progress = (pct / 100.0).toFloat(),
                modifier = Modifier
                    .fillMaxWidth()
                    .semantics {
                        contentDescription = "Predicted flashcard readiness ${pct.toInt()} percent"
                    },
            )
        }
    }
}

@Composable
private fun BreakdownCard(
    title: String,
    items: List<Triple<String, Double, Int>>,
) {
    CSNexusCard(modifier = Modifier.heightIn(min = 120.dp)) {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text(title, style = MaterialTheme.typography.titleMedium)
            if (items.isEmpty()) {
                Text("Not enough data yet.", color = MaterialTheme.colorScheme.onSurfaceVariant)
            } else {
                items.forEach { (label, retention, cardsStudied) ->
                    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                        ) {
                            Text(label)
                            Text("${retention.toInt()}%")
                        }
                        LuxuryProgressBar(progress = (retention / 100.0).toFloat(), modifier = Modifier.fillMaxWidth())
                        Text("$cardsStudied cards studied", color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
    }
}

@Composable
private fun HeatmapCard(heatmap: List<HeatmapEntryDto>) {
    CSNexusCard {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("Heatmap Summary", style = MaterialTheme.typography.titleMedium)
            heatmap.takeLast(7).forEach { entry ->
                Text(
                    "${entry.date}: ${entry.cardsReviewed} cards, ${entry.retentionRate.toInt()}% retention",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}
