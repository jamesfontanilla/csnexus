package com.csnexus.app.core.navigation

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.MenuBook
import androidx.compose.material.icons.filled.AccountCircle
import androidx.compose.material.icons.filled.AdminPanelSettings
import androidx.compose.material.icons.filled.Analytics
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Leaderboard
import androidx.compose.material.icons.filled.Psychology
import androidx.compose.material.icons.filled.Quiz
import androidx.compose.material.icons.filled.RocketLaunch
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Style
import androidx.compose.ui.graphics.vector.ImageVector

data class ShellDestination(
    val route: AppRoute,
    val label: String,
    val icon: ImageVector,
    val keywords: List<String>,
    val section: ShellDestinationSection,
    val bottomBar: Boolean = false,
    val adminOnly: Boolean = false,
)

enum class ShellDestinationSection(val label: String) {
    Primary("Pages"),
    Learning("Learning"),
    Account("Account"),
    Admin("Admin"),
}

val shellDestinations = listOf(
    ShellDestination(
        route = AppRoute.Dashboard,
        label = "Dashboard",
        icon = Icons.Filled.Home,
        keywords = listOf("home", "overview"),
        section = ShellDestinationSection.Primary,
        bottomBar = true,
    ),
    ShellDestination(
        route = AppRoute.Modules,
        label = "Modules",
        icon = Icons.AutoMirrored.Filled.MenuBook,
        keywords = listOf("subjects", "topics", "lessons"),
        section = ShellDestinationSection.Primary,
        bottomBar = true,
    ),
    ShellDestination(
        route = AppRoute.Quiz,
        label = "Quiz",
        icon = Icons.Filled.Quiz,
        keywords = listOf("practice", "questions"),
        section = ShellDestinationSection.Learning,
        bottomBar = true,
    ),
    ShellDestination(
        route = AppRoute.Flashcards,
        label = "Flashcards",
        icon = Icons.Filled.Style,
        keywords = listOf("cards", "deck", "study"),
        section = ShellDestinationSection.Learning,
    ),
    ShellDestination(
        route = AppRoute.Progress,
        label = "Progress",
        icon = Icons.Filled.Analytics,
        keywords = listOf("analytics", "stats", "performance"),
        section = ShellDestinationSection.Learning,
    ),
    ShellDestination(
        route = AppRoute.Analytics,
        label = "Analytics",
        icon = Icons.Filled.Analytics,
        keywords = listOf("trend", "accuracy", "heatmap"),
        section = ShellDestinationSection.Learning,
    ),
    ShellDestination(
        route = AppRoute.Mastery,
        label = "Mastery",
        icon = Icons.Filled.Quiz,
        keywords = listOf("reviews", "recommendations", "subtopics"),
        section = ShellDestinationSection.Learning,
    ),
    ShellDestination(
        route = AppRoute.Goals,
        label = "Goals",
        icon = Icons.Filled.RocketLaunch,
        keywords = listOf("daily", "streak", "target"),
        section = ShellDestinationSection.Learning,
    ),
    ShellDestination(
        route = AppRoute.StudyPlan,
        label = "Study Plan",
        icon = Icons.Filled.Home,
        keywords = listOf("planner", "tasks", "exam"),
        section = ShellDestinationSection.Learning,
    ),
    ShellDestination(
        route = AppRoute.Readiness,
        label = "Readiness",
        icon = Icons.Filled.Analytics,
        keywords = listOf("forecast", "probability", "confidence"),
        section = ShellDestinationSection.Learning,
    ),
    ShellDestination(
        route = AppRoute.Focus,
        label = "Focus",
        icon = Icons.Filled.Home,
        keywords = listOf("pomodoro", "timer", "deep work"),
        section = ShellDestinationSection.Learning,
    ),
    ShellDestination(
        route = AppRoute.Queue,
        label = "Queue",
        icon = Icons.Filled.Style,
        keywords = listOf("daily", "tasks", "study queue"),
        section = ShellDestinationSection.Learning,
    ),
    ShellDestination(
        route = AppRoute.Milestones,
        label = "Milestones",
        icon = Icons.Filled.RocketLaunch,
        keywords = listOf("achievements", "streak", "badges"),
        section = ShellDestinationSection.Learning,
    ),
    ShellDestination(
        route = AppRoute.Onboarding,
        label = "Onboarding",
        icon = Icons.Filled.AccountCircle,
        keywords = listOf("setup", "exam date", "study plan"),
        section = ShellDestinationSection.Account,
    ),
    ShellDestination(
        route = AppRoute.Leaderboards,
        label = "Leaderboard",
        icon = Icons.Filled.Leaderboard,
        keywords = listOf("ranking", "competition"),
        section = ShellDestinationSection.Learning,
    ),
    ShellDestination(
        route = AppRoute.Tournaments,
        label = "Tournaments",
        icon = Icons.Filled.Leaderboard,
        keywords = listOf("events", "prizes", "join"),
        section = ShellDestinationSection.Learning,
    ),
    ShellDestination(
        route = AppRoute.Tutor,
        label = "Tutor",
        icon = Icons.Filled.Psychology,
        keywords = listOf("chat", "ai", "help"),
        section = ShellDestinationSection.Learning,
    ),
    ShellDestination(
        route = AppRoute.Profile,
        label = "Profile",
        icon = Icons.Filled.AccountCircle,
        keywords = listOf("account", "user", "settings"),
        section = ShellDestinationSection.Account,
        bottomBar = true,
    ),
    ShellDestination(
        route = AppRoute.Settings,
        label = "Settings",
        icon = Icons.Filled.Settings,
        keywords = listOf("preferences", "account", "accessibility", "display"),
        section = ShellDestinationSection.Account,
    ),
    ShellDestination(
        route = AppRoute.Release,
        label = "Release Readiness",
        icon = Icons.Filled.RocketLaunch,
        keywords = listOf("build", "device", "apk", "quality"),
        section = ShellDestinationSection.Account,
    ),
    ShellDestination(
        route = AppRoute.Admin,
        label = "Admin",
        icon = Icons.Filled.AdminPanelSettings,
        keywords = listOf("users", "analytics", "management"),
        section = ShellDestinationSection.Admin,
        adminOnly = true,
    ),
)

fun filterShellDestinations(
    query: String,
    destinations: List<ShellDestination>,
): List<ShellDestination> {
    val normalizedQuery = query.trim().lowercase()
    if (normalizedQuery.isEmpty()) return destinations

    return destinations
        .mapNotNull { destination ->
            val haystack = buildList {
                add(destination.label)
                add(destination.route.route)
                addAll(destination.keywords)
            }.joinToString(" ").lowercase()
            val label = destination.label.lowercase()
            when {
                label.startsWith(normalizedQuery) -> 0 to destination
                haystack.contains(normalizedQuery) -> 1 to destination
                normalizedQuery.all { char -> haystack.contains(char) } -> 2 to destination
                else -> null
            }
        }
        .sortedWith(
            compareBy<Pair<Int, ShellDestination>> { it.first }
                .thenBy { it.second.label },
        )
        .map { it.second }
}
