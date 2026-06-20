package com.csnexus.app.feature.leaderboards.ui

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateMapOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.csnexus.app.core.design.CSNexusButton
import com.csnexus.app.core.design.CSNexusButtonVariant
import com.csnexus.app.core.design.CSNexusCard
import com.csnexus.app.core.design.CSNexusChip
import com.csnexus.app.core.design.CSNexusStatusBadge
import com.csnexus.app.core.design.CSNexusTabs
import com.csnexus.app.core.design.ErrorState
import com.csnexus.app.core.design.GlassLarge
import com.csnexus.app.core.design.GlassMedium
import com.csnexus.app.core.design.LoadingState
import com.csnexus.app.core.design.MetallicText
import com.csnexus.app.core.design.StaggeredItem
import com.csnexus.app.core.design.rememberCSNexusReducedMotion
import com.csnexus.app.core.error.userMessage
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.leaderboards.data.LeaderboardEntryDto
import com.csnexus.app.feature.leaderboards.data.LeaderboardRepository
import com.csnexus.app.feature.leaderboards.data.TournamentDto
import com.csnexus.app.feature.leaderboards.data.TournamentLeaderboardEntryDto
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

@Composable
fun LeaderboardsScreen(
    repository: LeaderboardRepository,
    contentPadding: PaddingValues,
    initialSection: CompetitionSection = CompetitionSection.Global,
) {
    val scope = rememberCoroutineScope()
    var selectedSectionIndex by remember(initialSection) { mutableIntStateOf(initialSection.ordinal) }
    var entries by remember { mutableStateOf<List<LeaderboardEntryDto>>(emptyList()) }
    var tournaments by remember { mutableStateOf<List<TournamentDto>>(emptyList()) }
    val tournamentLeaderboards = remember { mutableStateMapOf<Int, List<TournamentLeaderboardEntryDto>>() }
    var selectedTournamentId by remember { mutableStateOf<Int?>(null) }
    var leaderboardLoading by remember { mutableStateOf(false) }
    var tournamentsLoading by remember { mutableStateOf(false) }
    var leaderboardError by remember { mutableStateOf<String?>(null) }
    var tournamentError by remember { mutableStateOf<String?>(null) }
    var selectedCategory by remember { mutableStateOf<String?>(null) }
    var joiningTournamentId by remember { mutableStateOf<Int?>(null) }
    var loadingTournamentLeaderboardId by remember { mutableStateOf<Int?>(null) }

    fun loadLeaderboard(force: Boolean = false) {
        if (leaderboardLoading) return
        if (!force && entries.isNotEmpty()) return
        leaderboardLoading = true
        leaderboardError = null
        scope.launch {
            when (val result = repository.xp()) {
                is ApiResult.Success -> entries = result.value
                is ApiResult.Failure -> leaderboardError = result.error.userMessage()
            }
            leaderboardLoading = false
        }
    }

    fun loadTournaments(force: Boolean = false) {
        if (tournamentsLoading) return
        if (!force && tournaments.isNotEmpty()) return
        tournamentsLoading = true
        tournamentError = null
        scope.launch {
            when (val result = repository.tournaments()) {
                is ApiResult.Success -> tournaments = result.value
                is ApiResult.Failure -> tournamentError = result.error.userMessage()
            }
            tournamentsLoading = false
        }
    }

    fun joinTournament(tournamentId: Int) {
        if (joiningTournamentId != null) return
        joiningTournamentId = tournamentId
        tournamentError = null
        scope.launch {
            when (val result = repository.joinTournament(tournamentId)) {
                is ApiResult.Success -> loadTournaments(force = true)
                is ApiResult.Failure -> tournamentError = result.error.userMessage()
            }
            joiningTournamentId = null
        }
    }

    fun loadTournamentLeaderboard(tournamentId: Int) {
        if (loadingTournamentLeaderboardId == tournamentId) return
        loadingTournamentLeaderboardId = tournamentId
        selectedTournamentId = tournamentId
        tournamentError = null
        scope.launch {
            when (val result = repository.tournamentLeaderboard(tournamentId)) {
                is ApiResult.Success -> tournamentLeaderboards[tournamentId] = result.value
                is ApiResult.Failure -> tournamentError = result.error.userMessage()
            }
            loadingTournamentLeaderboardId = null
        }
    }

    LaunchedEffect(selectedSectionIndex) {
        when (CompetitionSection.entries[selectedSectionIndex]) {
            CompetitionSection.Global -> loadLeaderboard()
            CompetitionSection.Tournaments -> loadTournaments()
        }
    }

    val categories = remember(entries) { leaderboardCategories(entries) }
    val filteredEntries = remember(entries, selectedCategory) { filterLeaderboardEntries(entries, selectedCategory) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(contentPadding),
    ) {
        CSNexusTabs(
            tabs = CompetitionSection.entries.map { it.label },
            selectedIndex = selectedSectionIndex,
            onSelected = { selectedSectionIndex = it },
        )
        when (CompetitionSection.entries[selectedSectionIndex]) {
            CompetitionSection.Global -> LeaderboardTab(
                loading = leaderboardLoading,
                error = leaderboardError,
                entries = filteredEntries,
                categories = categories,
                selectedCategory = selectedCategory,
                onSelectCategory = { selectedCategory = it },
                onRetry = { loadLeaderboard(force = true) },
            )
            CompetitionSection.Tournaments -> TournamentsTab(
                loading = tournamentsLoading,
                error = tournamentError,
                tournaments = tournaments,
                selectedTournamentId = selectedTournamentId,
                tournamentLeaderboards = tournamentLeaderboards,
                joiningTournamentId = joiningTournamentId,
                loadingTournamentLeaderboardId = loadingTournamentLeaderboardId,
                onJoin = ::joinTournament,
                onOpenLeaderboard = ::loadTournamentLeaderboard,
                onRetry = { loadTournaments(force = true) },
            )
        }
    }
}

@Composable
private fun LeaderboardTab(
    loading: Boolean,
    error: String?,
    entries: List<LeaderboardEntryDto>,
    categories: List<String>,
    selectedCategory: String?,
    onSelectCategory: (String?) -> Unit,
    onRetry: () -> Unit,
) {
    if (loading && entries.isEmpty()) {
        LoadingState(label = "Loading leaderboard", modifier = Modifier.fillMaxSize())
        return
    }
    if (error != null && entries.isEmpty()) {
        ErrorState(message = error, onRetry = onRetry, modifier = Modifier.fillMaxSize())
        return
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                MetallicText(
                    text = "Leaderboard",
                    style = MaterialTheme.typography.headlineLarge,
                )
                Text(
                    "Top performers, tournament standings, and your current rank.",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                if (categories.isNotEmpty()) {
                    Row(
                        modifier = Modifier.horizontalScroll(rememberScrollState()),
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        CSNexusChip(
                            text = "All",
                            selected = selectedCategory == null,
                            onClick = { onSelectCategory(null) },
                        )
                        categories.forEach { category ->
                            CSNexusChip(
                                text = category,
                                selected = selectedCategory == category,
                                onClick = { onSelectCategory(category) },
                            )
                        }
                    }
                }
            }
        }
        if (error != null) {
            item {
                CompetitionErrorCard(message = error, onRetry = onRetry)
            }
        }
        if (entries.isEmpty()) {
            item {
                CompetitionEmptyCard(
                    title = "No rankings yet",
                    body = "Be the first learner to land on the board.",
                )
            }
        } else {
            // Top-3 podium section with spring-in entrance
            val podium = entries.take(3)
            if (podium.size == 3) {
                item {
                    PodiumSection(podium = podium)
                }
            }

            // Full leaderboard table in GlassLarge card
            item {
                GlassLarge(modifier = Modifier.fillMaxWidth()) {
                    Column(
                        modifier = Modifier.padding(vertical = 8.dp),
                        verticalArrangement = Arrangement.spacedBy(0.dp),
                    ) {
                        LeaderboardHeaderRow()
                        HorizontalDivider(color = Color.White.copy(alpha = 0.06f))
                        entries.forEachIndexed { index, entry ->
                            StaggeredItem(index = index) {
                                LeaderboardRow(
                                    entry = entry,
                                    index = index,
                                )
                            }
                            if (index < entries.lastIndex) {
                                HorizontalDivider(color = Color.White.copy(alpha = 0.06f))
                            }
                        }
                    }
                }
            }
        }
    }
}

/**
 * Top-3 podium displayed as 3 GlassMedium cards in a Row.
 * Layout order: Silver (2nd) | Gold (1st, larger) | Bronze (3rd).
 * Each card has a spring-in scale entrance animation.
 */
@Composable
private fun PodiumSection(podium: List<LeaderboardEntryDto>) {
    val reducedMotion = rememberCSNexusReducedMotion()

    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(10.dp),
        verticalAlignment = Alignment.Bottom,
    ) {
        // Display order: Silver (index 1), Gold (index 0), Bronze (index 2)
        val displayOrder = listOf(1, 0, 2)
        val medals = listOf("🥈", "🥇", "🥉")
        val weights = listOf(1f, 1.2f, 1f)

        displayOrder.forEachIndexed { displayIndex, entryIndex ->
            PodiumCard(
                modifier = Modifier.weight(weights[displayIndex]),
                medal = medals[displayIndex],
                entry = podium[entryIndex],
                delayMs = displayIndex * 100L,
                reducedMotion = reducedMotion,
            )
        }
    }
}

/**
 * Single podium card with spring-in scale animation.
 */
@Composable
private fun PodiumCard(
    modifier: Modifier = Modifier,
    medal: String,
    entry: LeaderboardEntryDto,
    delayMs: Long,
    reducedMotion: Boolean,
) {
    val scale = remember { Animatable(if (reducedMotion) 1f else 0f) }
    val alpha = remember { Animatable(if (reducedMotion) 1f else 0f) }

    LaunchedEffect(Unit) {
        if (!reducedMotion) {
            delay(delayMs)
            launch {
                scale.animateTo(
                    targetValue = 1f,
                    animationSpec = spring(
                        dampingRatio = Spring.DampingRatioMediumBouncy,
                        stiffness = Spring.StiffnessMedium,
                    ),
                )
            }
            launch {
                alpha.animateTo(
                    targetValue = 1f,
                    animationSpec = spring(
                        dampingRatio = Spring.DampingRatioNoBouncy,
                        stiffness = Spring.StiffnessMedium,
                    ),
                )
            }
        }
    }

    GlassMedium(
        modifier = modifier
            .graphicsLayer {
                scaleX = scale.value
                scaleY = scale.value
            }
            .alpha(alpha.value),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(14.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Text(
                text = medal,
                style = MaterialTheme.typography.headlineLarge,
            )
            Text(
                text = entry.displayName,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold,
                textAlign = TextAlign.Center,
                maxLines = 2,
            )
            Text(
                text = "${entry.score} XP",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.primary,
            )
            Text(
                text = "Level ${entry.level}",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun TournamentsTab(
    loading: Boolean,
    error: String?,
    tournaments: List<TournamentDto>,
    selectedTournamentId: Int?,
    tournamentLeaderboards: Map<Int, List<TournamentLeaderboardEntryDto>>,
    joiningTournamentId: Int?,
    loadingTournamentLeaderboardId: Int?,
    onJoin: (Int) -> Unit,
    onOpenLeaderboard: (Int) -> Unit,
    onRetry: () -> Unit,
) {
    if (loading && tournaments.isEmpty()) {
        LoadingState(label = "Loading tournaments", modifier = Modifier.fillMaxSize())
        return
    }
    if (error != null && tournaments.isEmpty()) {
        ErrorState(message = error, onRetry = onRetry, modifier = Modifier.fillMaxSize())
        return
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            MetallicText(
                text = "Tournaments",
                style = MaterialTheme.typography.headlineLarge,
            )
        }
        if (error != null) {
            item { CompetitionErrorCard(message = error, onRetry = onRetry) }
        }
        if (tournaments.isEmpty()) {
            item {
                CompetitionEmptyCard(
                    title = "No active tournaments",
                    body = "The web app is quiet here too until the backend opens a competition window.",
                )
            }
        } else {
            itemsIndexed(tournaments, key = { _, t -> t.id }) { index, tournament ->
                StaggeredItem(index = index) {
                    GlassMedium(modifier = Modifier.fillMaxWidth()) {
                        Column(
                            modifier = Modifier.padding(16.dp),
                            verticalArrangement = Arrangement.spacedBy(10.dp),
                        ) {
                            Row(
                                modifier = Modifier.fillMaxWidth(),
                                horizontalArrangement = Arrangement.SpaceBetween,
                            ) {
                                Column(modifier = Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                                    Text(tournament.title, style = MaterialTheme.typography.titleMedium)
                                    tournament.description?.takeIf(String::isNotBlank)?.let {
                                        Text(it, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                    }
                                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                        tournament.category?.takeIf(String::isNotBlank)?.let { CSNexusChip(text = it) }
                                        tournament.prizeDescription?.takeIf(String::isNotBlank)?.let { CSNexusChip(text = it) }
                                    }
                                }
                                CSNexusStatusBadge(
                                    text = tournamentCountdownLabel(
                                        tournament = tournament,
                                        nowMillis = System.currentTimeMillis(),
                                    ),
                                )
                            }
                            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                                CSNexusButton(
                                    text = if (joiningTournamentId == tournament.id) "Joining..." else "Join",
                                    onClick = { onJoin(tournament.id) },
                                    enabled = joiningTournamentId == null,
                                )
                                CSNexusButton(
                                    text = if (loadingTournamentLeaderboardId == tournament.id) "Loading..." else "Leaderboard",
                                    onClick = { onOpenLeaderboard(tournament.id) },
                                    variant = CSNexusButtonVariant.Secondary,
                                    enabled = loadingTournamentLeaderboardId == null,
                                )
                            }
                            val showBoard = selectedTournamentId == tournament.id
                            val board = tournamentLeaderboards[tournament.id].orEmpty()
                            if (showBoard) {
                                if (board.isEmpty() && loadingTournamentLeaderboardId == tournament.id) {
                                    Text("Loading tournament leaderboard...", color = MaterialTheme.colorScheme.onSurfaceVariant)
                                } else if (board.isEmpty()) {
                                    Text("No tournament standings yet.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                                } else {
                                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                        board.forEach { entry ->
                                            Row(
                                                modifier = Modifier.fillMaxWidth(),
                                                horizontalArrangement = Arrangement.SpaceBetween,
                                            ) {
                                                Text(
                                                    "#${entry.rank} ${entry.displayName ?: "User ${entry.userId}"}",
                                                    fontWeight = if (entry.isCurrentUser) FontWeight.SemiBold else FontWeight.Normal,
                                                )
                                                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                                    if (entry.isCurrentUser) {
                                                        CSNexusChip(text = "You")
                                                    }
                                                    Text("${entry.xpEarned} XP")
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

// Glass-medium background color for top-3 row highlighting
private val GlassMediumHighlight = Color(0x10FFFFFF) // 6% white — matches GlassMedium bg

@Composable
private fun LeaderboardHeaderRow() {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 14.dp, vertical = 10.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
    ) {
        Text(
            "#",
            modifier = Modifier.weight(0.18f),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            style = MaterialTheme.typography.labelLarge,
        )
        Text(
            "Name",
            modifier = Modifier.weight(0.42f),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            style = MaterialTheme.typography.labelLarge,
        )
        Text(
            "Level",
            modifier = Modifier.weight(0.18f),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            style = MaterialTheme.typography.labelLarge,
        )
        Text(
            "XP",
            modifier = Modifier.weight(0.22f),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            style = MaterialTheme.typography.labelLarge,
        )
    }
}

@Composable
private fun LeaderboardRow(
    entry: LeaderboardEntryDto,
    index: Int,
) {
    val rank = entry.rank.takeIf { it > 0 } ?: (index + 1)
    val highlight = entry.isCurrentUser
    val isTopThree = rank <= 3

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .background(
                when {
                    highlight -> MaterialTheme.colorScheme.primary.copy(alpha = 0.08f)
                    isTopThree -> GlassMediumHighlight
                    else -> Color.Transparent
                },
            )
            .padding(horizontal = 14.dp, vertical = 12.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
    ) {
        Text(
            text = when (rank) {
                1 -> "🥇"
                2 -> "🥈"
                3 -> "🥉"
                else -> "#$rank"
            },
            modifier = Modifier.weight(0.18f),
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            fontWeight = FontWeight.SemiBold,
        )
        Column(modifier = Modifier.weight(0.42f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(
                entry.displayName,
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = if (isTopThree || highlight) FontWeight.SemiBold else FontWeight.Normal,
            )
            if (entry.category.isNotBlank()) {
                CSNexusChip(text = entry.category)
            }
        }
        Text(
            "L${entry.level}",
            modifier = Modifier.weight(0.18f),
            color = MaterialTheme.colorScheme.primary,
            fontWeight = FontWeight.SemiBold,
        )
        Row(modifier = Modifier.weight(0.22f), horizontalArrangement = Arrangement.End) {
            Text(
                "${entry.score} XP",
                fontWeight = FontWeight.SemiBold,
            )
        }
    }
}

@Composable
private fun CompetitionErrorCard(
    message: String,
    onRetry: () -> Unit,
) {
    CSNexusCard {
        Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Text("Couldn't refresh competition data", style = MaterialTheme.typography.titleMedium)
            Text(message, color = MaterialTheme.colorScheme.onSurfaceVariant)
            CSNexusButton(
                text = "Retry",
                onClick = onRetry,
                variant = CSNexusButtonVariant.Secondary,
            )
        }
    }
}

@Composable
private fun CompetitionEmptyCard(
    title: String,
    body: String,
) {
    CSNexusCard {
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            Text(title, style = MaterialTheme.typography.titleMedium)
            Text(body, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}
