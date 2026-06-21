package com.csnexus.app.core.navigation

import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.ui.graphics.Color
import com.csnexus.app.core.design.GlassBottomNav
import com.csnexus.app.core.design.GlassBottomNavItem
import com.csnexus.app.core.design.GlassToast
import com.csnexus.app.core.design.GlassToastState
import com.csnexus.app.core.design.GlassToastVariant
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.dp
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.csnexus.app.core.auth.AuthState
import com.csnexus.app.core.design.CSNexusMotion
import com.csnexus.app.core.design.rememberCSNexusReducedMotion
import com.csnexus.app.core.di.AppContainer
import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.feature.admin.ui.AdminDashboardScreen
import com.csnexus.app.feature.auth.ui.ForgotPasswordScreen
import com.csnexus.app.feature.auth.ui.LoginScreen
import com.csnexus.app.feature.auth.ui.OtpVerificationScreen
import com.csnexus.app.feature.auth.ui.SignupScreen
import com.csnexus.app.feature.content.ui.ModuleListScreen
import com.csnexus.app.feature.content.ui.LessonReaderScreen
import com.csnexus.app.feature.content.ui.SubtopicListScreen
import com.csnexus.app.feature.content.ui.TopicListScreen
import com.csnexus.app.feature.dashboard.ui.DashboardScreen
import com.csnexus.app.feature.flashcards.ui.FlashcardsScreen
import com.csnexus.app.feature.flashcards.ui.FlashcardAdminScreen
import com.csnexus.app.feature.flashcards.ui.FlashcardAnalyticsScreen
import com.csnexus.app.feature.flashcards.ui.FlashcardCreateDeckScreen
import com.csnexus.app.feature.flashcards.ui.FlashcardDeckDetailScreen
import com.csnexus.app.feature.flashcards.ui.FlashcardExamScreen
import com.csnexus.app.feature.flashcards.ui.FlashcardGenerateScreen
import com.csnexus.app.feature.flashcards.ui.FlashcardMarketplaceScreen
import com.csnexus.app.feature.flashcards.ui.FlashcardSocialScreen
import com.csnexus.app.feature.flashcards.ui.FlashcardStudyScreen
import com.csnexus.app.feature.home.ui.PublicHomeScreen
import com.csnexus.app.feature.leaderboards.ui.LeaderboardsScreen
import com.csnexus.app.feature.leaderboards.ui.CompetitionSection
import com.csnexus.app.feature.mockexam.ui.MockExamScreen
import com.csnexus.app.feature.motivation.ui.FocusScreen
import com.csnexus.app.feature.motivation.ui.MilestonesScreen
import com.csnexus.app.feature.motivation.ui.OnboardingScreen
import com.csnexus.app.feature.motivation.ui.QueueScreen
import com.csnexus.app.feature.profile.ui.ProfileScreen
import com.csnexus.app.feature.progress.ui.ProgressScreen
import com.csnexus.app.feature.progress.ui.ProgressSection
import com.csnexus.app.feature.quizzes.ui.QuizScreen
import com.csnexus.app.feature.quizzes.data.QuizScope
import com.csnexus.app.feature.release.ui.ReleaseReadinessScreen
import com.csnexus.app.feature.settings.ui.SettingsScreen
import com.csnexus.app.feature.tutor.ui.TutorScreen
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CSNexusNavGraph(container: AppContainer) {
    val navController = rememberNavController()
    val authState by container.sessionManager.authState.collectAsState()
    val isAuthenticated = authState != AuthState.Unauthenticated
    val startDestination = if (isAuthenticated) AppRoute.Dashboard.route else AppRoute.Home.route
    val backStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = backStackEntry?.destination
    val currentRoute = currentDestination?.route
    var toastState by remember { mutableStateOf<GlassToastState?>(null) }
    var quickNavOpen by remember { mutableStateOf(false) }
    var isAdmin by remember { mutableStateOf(false) }
    var accountError by remember { mutableStateOf<String?>(null) }
    val availableDestinations = remember(isAdmin) {
        shellDestinations.filter { !it.adminOnly || isAdmin }
    }
    val bottomDestinations = availableDestinations.filter { it.bottomBar }
    val reducedMotion = rememberCSNexusReducedMotion()
    val density = LocalDensity.current

    LaunchedEffect(Unit) {
        container.sessionManager.initializeFromStore()
    }

    LaunchedEffect(authState) {
        val activeRoute = navController.currentBackStackEntry?.destination?.route
        when (authState) {
            AuthState.Authenticated -> {
                if (activeRoute == AppRoute.Login.route) {
                    navController.navigate(AppRoute.Dashboard.route) {
                        popUpTo(AppRoute.Login.route) { inclusive = true }
                    }
                }
            }
            AuthState.Refreshing -> Unit
            AuthState.Unauthenticated -> {
                isAdmin = false
                if (activeRoute != null && activeRoute !in publicAuthRoutes) {
                    navController.navigate(AppRoute.Login.route) {
                        popUpTo(0)
                    }
                }
            }
        }
    }

    LaunchedEffect(isAuthenticated) {
        if (!isAuthenticated) {
            isAdmin = false
            return@LaunchedEffect
        }

        when (val result = container.authRepository.currentUser()) {
            is ApiResult.Success -> {
                isAdmin = result.value.role.equals("admin", ignoreCase = true)
                accountError = null
            }
            is ApiResult.Failure -> {
                isAdmin = false
                accountError = "Could not load account permissions."
            }
        }
    }

    LaunchedEffect(accountError) {
        accountError?.let {
            toastState = GlassToastState(
                message = it,
                variant = GlassToastVariant.Error,
            )
        }
    }

    LaunchedEffect(currentRoute) {
        currentRoute?.let { route ->
            container.logger.screenView(
                screenName = route.titleForRoute(),
                route = route,
            )
        }
    }

    if (quickNavOpen) {
        QuickNavigationSheet(
            destinations = availableDestinations,
            onNavigate = { destination ->
                quickNavOpen = false
                navController.navigateTopLevel(destination.route)
            },
            onDismiss = { quickNavOpen = false },
        )
    }

    Box(modifier = Modifier.fillMaxSize()) {
        Scaffold(
            containerColor = Color.Transparent,
            topBar = {
            if (isAuthenticated) {
                TopAppBar(
                    title = { Text(currentRoute.titleForRoute()) },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = Color.Transparent,
                        scrolledContainerColor = Color.Transparent,
                        titleContentColor = MaterialTheme.colorScheme.onBackground,
                        navigationIconContentColor = MaterialTheme.colorScheme.onBackground,
                        actionIconContentColor = MaterialTheme.colorScheme.onBackground,
                    ),
                    navigationIcon = {
                        if (currentRoute.shouldShowBackButton()) {
                            IconButton(onClick = { navController.popBackStack() }) {
                                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                            }
                        }
                    },
                    actions = {
                        IconButton(onClick = { quickNavOpen = true }) {
                            Icon(Icons.Filled.Search, contentDescription = "Open quick navigation")
                        }
                    },
                )
                if (authState == AuthState.Refreshing) {
                    LinearProgressIndicator()
                }
            }
        },
        bottomBar = {
            if (isAuthenticated) {
                GlassBottomNav(
                    items = bottomDestinations.map { destination ->
                        GlassBottomNavItem(
                            icon = destination.icon,
                            label = destination.label,
                            selected = currentDestination?.hierarchy?.any {
                                it.route == destination.route.route
                            } == true,
                            onClick = { navController.navigateTopLevel(destination.route) },
                        )
                    },
                )
            }
        },
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = startDestination,
            enterTransition = {
                if (reducedMotion) {
                    fadeIn(animationSpec = tween(CSNexusMotion.DurationPage))
                } else {
                    fadeIn(animationSpec = tween(CSNexusMotion.DurationPage, easing = FastOutSlowInEasing)) +
                        slideInVertically(
                            animationSpec = tween(CSNexusMotion.DurationPage, easing = FastOutSlowInEasing),
                            initialOffsetY = { with(density) { 12.dp.roundToPx() } },
                        )
                }
            },
            exitTransition = {
                fadeOut(animationSpec = tween(CSNexusMotion.DurationFast))
            },
            popEnterTransition = {
                if (reducedMotion) {
                    fadeIn(animationSpec = tween(CSNexusMotion.DurationPage))
                } else {
                    fadeIn(animationSpec = tween(CSNexusMotion.DurationPage, easing = FastOutSlowInEasing)) +
                        slideInVertically(
                            animationSpec = tween(CSNexusMotion.DurationPage, easing = FastOutSlowInEasing),
                            initialOffsetY = { with(density) { 12.dp.roundToPx() } },
                        )
                }
            },
            popExitTransition = {
                fadeOut(animationSpec = tween(CSNexusMotion.DurationFast))
            },
        ) {
            composable(AppRoute.Home.route) {
                PublicHomeScreen(
                    contentPadding = innerPadding,
                    isAuthenticated = isAuthenticated,
                    onContinueStudying = { navController.navigateTopLevel(AppRoute.Dashboard) },
                    onSignup = { navController.navigate(AppRoute.Signup.route) },
                    onLogin = { navController.navigate(AppRoute.Login.route) },
                )
            }
            composable(AppRoute.Login.route) {
                LoginScreen(
                    authRepository = container.authRepository,
                    googleServerClientId = container.googleServerClientId,
                    onAuthenticated = {
                        navController.navigate(AppRoute.Dashboard.route) {
                            popUpTo(AppRoute.Login.route) { inclusive = true }
                        }
                    },
                    onSignup = { navController.navigate(AppRoute.Signup.route) },
                    onForgotPassword = { navController.navigate(AppRoute.ForgotPassword.route) },
                )
            }
            composable(AppRoute.Signup.route) {
                SignupScreen(
                    authRepository = container.authRepository,
                    onOtpRequired = { email ->
                        navController.navigate(AppRoute.VerifyOtp.create(email, "VERIFY_EMAIL"))
                    },
                    onLogin = {
                        navController.navigate(AppRoute.Login.route) {
                            popUpTo(AppRoute.Login.route) { inclusive = false }
                        }
                    },
                )
            }
            composable(AppRoute.ForgotPassword.route) {
                ForgotPasswordScreen(
                    authRepository = container.authRepository,
                    onEnterCode = { email ->
                        navController.navigate(AppRoute.VerifyOtp.create(email, "PASSWORD_RESET"))
                    },
                    onLogin = {
                        navController.navigate(AppRoute.Login.route) {
                            popUpTo(AppRoute.Login.route) { inclusive = false }
                        }
                    },
                )
            }
            composable(
                route = AppRoute.VerifyOtp.route,
                arguments = listOf(
                    navArgument("purpose") { type = NavType.StringType },
                    navArgument("email") { type = NavType.StringType },
                ),
            ) { backStackEntry ->
                OtpVerificationScreen(
                    authRepository = container.authRepository,
                    email = backStackEntry.arguments?.getString("email").orEmpty(),
                    purpose = backStackEntry.arguments?.getString("purpose").orEmpty(),
                    onAuthenticated = {
                        navController.navigate(AppRoute.Dashboard.route) {
                            popUpTo(AppRoute.Login.route) { inclusive = true }
                        }
                    },
                    onLogin = {
                        navController.navigate(AppRoute.Login.route) {
                            popUpTo(AppRoute.Login.route) { inclusive = false }
                        }
                    },
                )
            }
            composable(AppRoute.Dashboard.route) {
                DashboardScreen(
                    contentPadding = innerPadding,
                    onOpenModules = { navController.navigate(AppRoute.Modules.route) },
                    onOpenQuiz = { navController.navigate(AppRoute.Quiz.route) },
                    onOpenMockExam = { navController.navigate(AppRoute.MockExam.route) },
                    onOpenFlashcards = { navController.navigate(AppRoute.Flashcards.route) },
                    onOpenLeaderboards = { navController.navigate(AppRoute.Leaderboards.route) },
                    onOpenProgress = { navController.navigate(AppRoute.Progress.route) },
                    onOpenFocus = { navController.navigate(AppRoute.Focus.route) },
                    onOpenQueue = { navController.navigate(AppRoute.Queue.route) },
                    onOpenMilestones = { navController.navigate(AppRoute.Milestones.route) },
                    onOpenOnboarding = { navController.navigate(AppRoute.Onboarding.route) },
                    onOpenTutor = { navController.navigate(AppRoute.Tutor.route) },
                    onOpenRelease = { navController.navigate(AppRoute.Release.route) },
                )
            }
            composable(AppRoute.Modules.route) {
                ModuleListScreen(
                    repository = container.contentRepository,
                    contentPadding = innerPadding,
                    onModuleSelected = { moduleId ->
                        navController.navigate(AppRoute.Topics.create(moduleId))
                    },
                )
            }
            composable(AppRoute.Topics.route) { backStackEntry ->
                val moduleId = backStackEntry.arguments?.getString("moduleId")?.toIntOrNull() ?: 0
                TopicListScreen(
                    repository = container.contentRepository,
                    moduleId = moduleId,
                    contentPadding = innerPadding,
                    onTopicSelected = { topicId ->
                        navController.navigate(AppRoute.Subtopics.create(topicId))
                    },
                    onModuleQuizSelected = { id ->
                        navController.navigate(AppRoute.ScopedQuiz.create("module", id))
                    },
                )
            }
            composable(AppRoute.Subtopics.route) { backStackEntry ->
                val topicId = backStackEntry.arguments?.getString("topicId")?.toIntOrNull() ?: 0
                SubtopicListScreen(
                    repository = container.contentRepository,
                    topicId = topicId,
                    contentPadding = innerPadding,
                    onSubtopicSelected = { subtopicId ->
                        navController.navigate(AppRoute.Lesson.create(subtopicId))
                    },
                    onTopicQuizSelected = { id ->
                        navController.navigate(AppRoute.ScopedQuiz.create("topic", id))
                    },
                    onSubtopicQuizSelected = { id ->
                        navController.navigate(AppRoute.ScopedQuiz.create("subtopic", id))
                    },
                )
            }
            composable(AppRoute.Lesson.route) { backStackEntry ->
                val subtopicId = backStackEntry.arguments?.getString("subtopicId")?.toIntOrNull() ?: 0
                LessonReaderScreen(
                    repository = container.contentRepository,
                    tutorRepository = container.tutorRepository,
                    subtopicId = subtopicId,
                    contentPadding = innerPadding,
                )
            }
            composable(AppRoute.Quiz.route) {
                QuizScreen(
                    repository = container.quizRepository,
                    contentPadding = innerPadding,
                    onOpenLesson = { subtopicId -> navController.navigate(AppRoute.Lesson.create(subtopicId)) },
                    onBackToModules = { navController.navigate(AppRoute.Modules.route) },
                )
            }
            composable(
                route = AppRoute.ScopedQuiz.route,
                arguments = listOf(
                    navArgument("scope") { type = NavType.StringType },
                    navArgument("scopeId") { type = NavType.StringType },
                ),
            ) { backStackEntry ->
                val scope = QuizScope.from(backStackEntry.arguments?.getString("scope").orEmpty())
                val scopeId = backStackEntry.arguments?.getString("scopeId")?.toIntOrNull() ?: 1
                QuizScreen(
                    repository = container.quizRepository,
                    contentPadding = innerPadding,
                    scope = scope,
                    scopeId = scopeId,
                    onOpenLesson = { subtopicId -> navController.navigate(AppRoute.Lesson.create(subtopicId)) },
                    onBackToModules = { navController.navigate(AppRoute.Modules.route) },
                )
            }
            composable(AppRoute.MockExam.route) {
                MockExamScreen(
                    repository = container.mockExamRepository,
                    contentPadding = innerPadding,
                )
            }
            composable(AppRoute.Flashcards.route) {
                FlashcardsScreen(
                    repository = container.flashcardRepository,
                    contentPadding = innerPadding,
                    onOpenCreateDeck = { navController.navigate(AppRoute.FlashcardsCreateDeck.route) },
                    onOpenDeck = { deckId -> navController.navigate(AppRoute.FlashcardsDeckDetail.create(deckId)) },
                    onOpenStudy = { deckIds, mode ->
                        navController.navigate(AppRoute.FlashcardsStudy.create(deckIds, mode?.name?.lowercase(Locale.US)))
                    },
                    onOpenMarketplace = { navController.navigate(AppRoute.FlashcardsMarketplace.route) },
                    onOpenAnalytics = { navController.navigate(AppRoute.FlashcardsAnalytics.route) },
                    onOpenExam = { navController.navigate(AppRoute.FlashcardsExam.route) },
                    onOpenSocial = { navController.navigate(AppRoute.FlashcardsSocial.route) },
                    onOpenGenerate = { navController.navigate(AppRoute.FlashcardsGenerate.route) },
                )
            }
            composable(AppRoute.FlashcardsCreateDeck.route) {
                FlashcardCreateDeckScreen(
                    repository = container.flashcardRepository,
                    contentPadding = innerPadding,
                    onCreated = { deckId ->
                        navController.navigate(AppRoute.FlashcardsDeckDetail.create(deckId)) {
                            popUpTo(AppRoute.FlashcardsCreateDeck.route) { inclusive = true }
                        }
                    },
                )
            }
            composable(AppRoute.FlashcardsDeckDetail.route) { backStackEntry ->
                val deckId = backStackEntry.arguments?.getString("deckId")?.toIntOrNull() ?: 0
                FlashcardDeckDetailScreen(
                    repository = container.flashcardRepository,
                    deckId = deckId,
                    contentPadding = innerPadding,
                    onStudyDeck = { deckIds, mode ->
                        navController.navigate(AppRoute.FlashcardsStudy.create(deckIds, mode?.name?.lowercase(Locale.US)))
                    },
                )
            }
            composable(
                route = AppRoute.FlashcardsStudy.route,
                arguments = listOf(
                    navArgument("deckIds") {
                        type = NavType.StringType
                        nullable = true
                        defaultValue = ""
                    },
                    navArgument("mode") {
                        type = NavType.StringType
                        nullable = true
                        defaultValue = ""
                    },
                ),
            ) { backStackEntry ->
                val deckIds = backStackEntry.arguments
                    ?.getString("deckIds")
                    .orEmpty()
                    .split(",")
                    .mapNotNull { it.toIntOrNull() }
                val mode = backStackEntry.arguments
                    ?.getString("mode")
                    .orEmpty()
                    .trim()
                    .lowercase(Locale.US)
                    .takeIf { it.isNotBlank() }
                    ?.let { raw ->
                        com.csnexus.app.feature.flashcards.data.FlashcardStudyMode.entries.firstOrNull {
                            it.name.lowercase(Locale.US) == raw
                        }
                    }
                FlashcardStudyScreen(
                    repository = container.flashcardRepository,
                    contentPadding = innerPadding,
                    deckIds = deckIds,
                    initialMode = mode,
                    onBack = { navController.popBackStack() },
                )
            }
            composable(AppRoute.FlashcardsMarketplace.route) {
                FlashcardMarketplaceScreen(
                    repository = container.flashcardRepository,
                    contentPadding = innerPadding,
                )
            }
            composable(AppRoute.FlashcardsAnalytics.route) {
                FlashcardAnalyticsScreen(
                    repository = container.flashcardRepository,
                    contentPadding = innerPadding,
                )
            }
            composable(AppRoute.FlashcardsExam.route) {
                FlashcardExamScreen(
                    repository = container.flashcardRepository,
                    contentPadding = innerPadding,
                )
            }
            composable(AppRoute.FlashcardsSocial.route) {
                FlashcardSocialScreen(
                    repository = container.flashcardRepository,
                    contentPadding = innerPadding,
                )
            }
            composable(AppRoute.FlashcardsGenerate.route) {
                FlashcardGenerateScreen(
                    repository = container.flashcardRepository,
                    contentPadding = innerPadding,
                )
            }
            composable(AppRoute.FlashcardsAdmin.route) {
                FlashcardAdminScreen(
                    repository = container.flashcardRepository,
                    contentPadding = innerPadding,
                    isAdmin = isAdmin,
                )
            }
            composable(AppRoute.Leaderboards.route) {
                LeaderboardsScreen(
                    repository = container.leaderboardRepository,
                    contentPadding = innerPadding,
                )
            }
            composable(AppRoute.Tournaments.route) {
                LeaderboardsScreen(
                    repository = container.leaderboardRepository,
                    contentPadding = innerPadding,
                    initialSection = CompetitionSection.Tournaments,
                )
            }
            composable(AppRoute.Progress.route) {
                ProgressScreen(
                    repository = container.progressRepository,
                    contentPadding = innerPadding,
                    onOpenModules = { navController.navigate(AppRoute.Modules.route) },
                )
            }
            composable(AppRoute.Analytics.route) {
                ProgressScreen(
                    repository = container.progressRepository,
                    contentPadding = innerPadding,
                    initialSection = ProgressSection.Analytics,
                    onOpenModules = { navController.navigate(AppRoute.Modules.route) },
                )
            }
            composable(AppRoute.Mastery.route) {
                ProgressScreen(
                    repository = container.progressRepository,
                    contentPadding = innerPadding,
                    initialSection = ProgressSection.Mastery,
                    onOpenModules = { navController.navigate(AppRoute.Modules.route) },
                )
            }
            composable(AppRoute.Goals.route) {
                ProgressScreen(
                    repository = container.progressRepository,
                    contentPadding = innerPadding,
                    initialSection = ProgressSection.Goals,
                    onOpenModules = { navController.navigate(AppRoute.Modules.route) },
                )
            }
            composable(AppRoute.StudyPlan.route) {
                ProgressScreen(
                    repository = container.progressRepository,
                    contentPadding = innerPadding,
                    initialSection = ProgressSection.StudyPlan,
                    onOpenModules = { navController.navigate(AppRoute.Modules.route) },
                )
            }
            composable(AppRoute.Readiness.route) {
                ProgressScreen(
                    repository = container.progressRepository,
                    contentPadding = innerPadding,
                    initialSection = ProgressSection.Readiness,
                    onOpenModules = { navController.navigate(AppRoute.Modules.route) },
                )
            }
            composable(AppRoute.Focus.route) {
                FocusScreen(
                    repository = container.motivationRepository,
                    contentPadding = innerPadding,
                )
            }
            composable(AppRoute.Queue.route) {
                QueueScreen(
                    repository = container.motivationRepository,
                    contentPadding = innerPadding,
                    onOpenLesson = { subtopicId -> navController.navigate(AppRoute.Lesson.create(subtopicId)) },
                    onOpenQuiz = { subtopicId -> navController.navigate(AppRoute.ScopedQuiz.create("subtopic", subtopicId)) },
                    onOpenFlashcards = { deckIds ->
                        navController.navigate(
                            AppRoute.FlashcardsStudy.create(
                                deckIds = deckIds,
                                mode = null,
                            ),
                        )
                    },
                )
            }
            composable(AppRoute.Milestones.route) {
                MilestonesScreen(
                    repository = container.motivationRepository,
                    progressRepository = container.progressRepository,
                    contentPadding = innerPadding,
                )
            }
            composable(AppRoute.Onboarding.route) {
                OnboardingScreen(
                    repository = container.motivationRepository,
                    contentPadding = innerPadding,
                    onCompleted = { navController.navigateTopLevel(AppRoute.Dashboard) },
                    onSkipped = { navController.navigateTopLevel(AppRoute.Dashboard) },
                )
            }
            composable(AppRoute.Tutor.route) {
                TutorScreen(
                    repository = container.tutorRepository,
                    contentRepository = container.contentRepository,
                    contentPadding = innerPadding,
                )
            }
            composable(AppRoute.Release.route) {
                ReleaseReadinessScreen(contentPadding = innerPadding)
            }
            composable(AppRoute.Admin.route) {
                AdminDashboardScreen(
                    contentPadding = innerPadding,
                    isAdmin = isAdmin,
                    adminRepository = container.adminRepository,
                )
            }
            composable(AppRoute.Profile.route) {
                ProfileScreen(
                    authRepository = container.authRepository,
                    progressRepository = container.progressRepository,
                    contentPadding = innerPadding,
                    onOpenSettings = { navController.navigateTopLevel(AppRoute.Settings) },
                    onLoggedOut = {
                        navController.navigate(AppRoute.Login.route) {
                            popUpTo(0)
                        }
                    },
                )
            }
            composable(AppRoute.Settings.route) {
                SettingsScreen(
                    authRepository = container.authRepository,
                    settingsRepository = container.settingsRepository,
                    contentPadding = innerPadding,
                    onLoggedOut = {
                        navController.navigate(AppRoute.Login.route) {
                            popUpTo(0)
                        }
                    },
                )
            }
        }
    }

        // Toast overlay at top-end
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            contentAlignment = Alignment.TopEnd,
        ) {
            GlassToast(
                state = toastState,
                onDismiss = { toastState = null },
            )
        }
    }
}

private fun androidx.navigation.NavHostController.navigateTopLevel(route: AppRoute) {
    navigate(route.route) {
        popUpTo(AppRoute.Dashboard.route) { saveState = true }
        launchSingleTop = true
        restoreState = true
    }
}

private fun String?.titleForRoute(): String {
    return when (this) {
        AppRoute.Home.route -> "Home"
        AppRoute.Dashboard.route -> "Dashboard"
        AppRoute.Modules.route -> "Modules"
        AppRoute.Quiz.route -> "Quiz"
        AppRoute.ScopedQuiz.route -> "Quiz"
        AppRoute.MockExam.route -> "Mock Exam"
        AppRoute.Flashcards.route -> "Flashcards"
        AppRoute.FlashcardsCreateDeck.route -> "Create Deck"
        AppRoute.FlashcardsDeckDetail.route -> "Deck Detail"
        AppRoute.FlashcardsStudy.route -> "Study Session"
        AppRoute.FlashcardsMarketplace.route -> "Marketplace"
        AppRoute.FlashcardsAnalytics.route -> "Flashcard Analytics"
        AppRoute.FlashcardsExam.route -> "Exam Simulation"
        AppRoute.FlashcardsSocial.route -> "Social"
        AppRoute.FlashcardsGenerate.route -> "Generate Cards"
        AppRoute.FlashcardsAdmin.route -> "Flashcard Admin"
        AppRoute.Leaderboards.route -> "Leaderboard"
        AppRoute.Tournaments.route -> "Tournaments"
        AppRoute.Progress.route -> "Progress"
        AppRoute.Analytics.route -> "Analytics"
        AppRoute.Mastery.route -> "Mastery"
        AppRoute.Goals.route -> "Goals"
        AppRoute.StudyPlan.route -> "Study Plan"
        AppRoute.Readiness.route -> "Readiness"
        AppRoute.Focus.route -> "Focus"
        AppRoute.Queue.route -> "Queue"
        AppRoute.Milestones.route -> "Milestones"
        AppRoute.Onboarding.route -> "Onboarding"
        AppRoute.Tutor.route -> "Tutor"
        AppRoute.Profile.route -> "Profile"
        AppRoute.Settings.route -> "Settings"
        AppRoute.Release.route -> "Release Readiness"
        AppRoute.Admin.route -> "Admin"
        AppRoute.Topics.route -> "Topics"
        AppRoute.Subtopics.route -> "Subtopics"
        AppRoute.Lesson.route -> "Lesson"
        else -> "CSNexus"
    }
}

private fun String?.shouldShowBackButton(): Boolean {
    return this != null && this !in shellDestinations.map { it.route.route }.toSet()
}

private val publicAuthRoutes = setOf(
    AppRoute.Home.route,
    AppRoute.Login.route,
    AppRoute.Signup.route,
    AppRoute.ForgotPassword.route,
    AppRoute.VerifyOtp.route,
)
