package com.csnexus.app.feature.quizzes.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun QuizPlaceholderScreen(contentPadding: PaddingValues) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding)
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        Text("Quiz", style = MaterialTheme.typography.headlineMedium)
        Text(
            "The native quiz player is next in the milestone-1 plan. It will use the existing quiz API rather than local-only scoring.",
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}
