package com.csnexus.app.core.design

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp

/** Dashboard skeleton: circle + stat cards + section bars */
@Composable
fun DashboardSkeleton(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        // Progress ring placeholder (160dp circle)
        CSNexusSkeleton(
            modifier = Modifier
                .size(160.dp)
                .clip(CircleShape),
        )
        // 3 stat card rectangles
        repeat(3) {
            CSNexusSkeleton(modifier = Modifier.fillMaxWidth().height(72.dp))
        }
        // 2 section bars
        repeat(2) {
            CSNexusSkeleton(modifier = Modifier.fillMaxWidth(0.6f).height(20.dp))
        }
    }
}

/** Module list skeleton: 6 cards (title 60% + description lines + progress bar) */
@Composable
fun ModuleListSkeleton(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        repeat(6) {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                // Title line 60%
                CSNexusSkeleton(modifier = Modifier.fillMaxWidth(0.6f).height(20.dp))
                // Description lines
                CSNexusSkeleton(modifier = Modifier.fillMaxWidth().height(14.dp))
                CSNexusSkeleton(modifier = Modifier.fillMaxWidth(0.8f).height(14.dp))
                // Progress bar
                CSNexusSkeleton(modifier = Modifier.fillMaxWidth().height(8.dp))
            }
        }
    }
}

/** Topic list skeleton: 4 card shapes (title 70% + subtitle 40%) */
@Composable
fun TopicListSkeleton(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        repeat(4) {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                CSNexusSkeleton(modifier = Modifier.fillMaxWidth(0.7f).height(20.dp))
                CSNexusSkeleton(modifier = Modifier.fillMaxWidth(0.4f).height(16.dp))
            }
        }
    }
}

/** Lesson reader skeleton: progress bar line + title (60%) + 2 content blocks (96dp height) */
@Composable
fun LessonSkeleton(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        CSNexusSkeleton(modifier = Modifier.fillMaxWidth().height(4.dp))
        CSNexusSkeleton(modifier = Modifier.fillMaxWidth(0.6f).height(24.dp))
        CSNexusSkeleton(modifier = Modifier.fillMaxWidth().height(96.dp))
        CSNexusSkeleton(modifier = Modifier.fillMaxWidth().height(96.dp))
    }
}

/** Readiness skeleton: 160dp circle + 4 card skeletons */
@Composable
fun ReadinessSkeleton(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        CSNexusSkeleton(modifier = Modifier.size(160.dp).clip(CircleShape))
        repeat(4) {
            CSNexusSkeleton(modifier = Modifier.fillMaxWidth().height(72.dp))
        }
    }
}

/** Flashcard deck skeleton: 4 deck-card skeletons (title + badge + count line) */
@Composable
fun FlashcardDecksSkeleton(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        repeat(4) {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                // Title
                CSNexusSkeleton(modifier = Modifier.fillMaxWidth(0.5f).height(20.dp))
                // Badge
                CSNexusSkeleton(modifier = Modifier.fillMaxWidth(0.3f).height(16.dp))
                // Count line
                CSNexusSkeleton(modifier = Modifier.fillMaxWidth(0.4f).height(14.dp))
            }
        }
    }
}
