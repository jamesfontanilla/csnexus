package com.csnexus.app.core.navigation

import android.net.Uri

sealed class AppRoute(val route: String) {
    data object Home : AppRoute("home")
    data object Login : AppRoute("login")
    data object Signup : AppRoute("signup")
    data object ForgotPassword : AppRoute("forgot-password")
    data object VerifyOtp : AppRoute("verify-otp/{purpose}/{email}") {
        fun create(email: String, purpose: String): String =
            "verify-otp/${Uri.encode(purpose)}/${Uri.encode(email)}"
    }
    data object Dashboard : AppRoute("dashboard")
    data object Modules : AppRoute("modules")
    data object Topics : AppRoute("modules/{moduleId}/topics") {
        fun create(moduleId: Int): String = "modules/$moduleId/topics"
    }
    data object Subtopics : AppRoute("topics/{topicId}/subtopics") {
        fun create(topicId: Int): String = "topics/$topicId/subtopics"
    }
    data object Lesson : AppRoute("subtopics/{subtopicId}/lesson") {
        fun create(subtopicId: Int): String = "subtopics/$subtopicId/lesson"
    }
    data object Profile : AppRoute("profile")
    data object Quiz : AppRoute("quiz")
    data object ScopedQuiz : AppRoute("quiz/{scope}/{scopeId}") {
        fun create(scope: String, scopeId: Int): String = "quiz/${Uri.encode(scope)}/$scopeId"
    }
    data object MockExam : AppRoute("mock-exam")
    data object Flashcards : AppRoute("flashcards")
    data object FlashcardsCreateDeck : AppRoute("flashcards/decks/new")
    data object FlashcardsDeckDetail : AppRoute("flashcards/decks/{deckId}") {
        fun create(deckId: Int): String = "flashcards/decks/$deckId"
    }
    data object FlashcardsStudy : AppRoute("flashcards/study?deckIds={deckIds}&mode={mode}") {
        fun create(deckIds: List<Int> = emptyList(), mode: String? = null): String {
            val deckIdsValue = deckIds.joinToString(",")
            val modeValue = mode ?: ""
            return "flashcards/study?deckIds=${Uri.encode(deckIdsValue)}&mode=${Uri.encode(modeValue)}"
        }
    }
    data object FlashcardsMarketplace : AppRoute("flashcards/marketplace")
    data object FlashcardsAnalytics : AppRoute("flashcards/analytics")
    data object FlashcardsExam : AppRoute("flashcards/exam")
    data object FlashcardsSocial : AppRoute("flashcards/social")
    data object FlashcardsGenerate : AppRoute("flashcards/generate")
    data object FlashcardsAdmin : AppRoute("flashcards/admin")
    data object Leaderboards : AppRoute("leaderboards")
    data object Tournaments : AppRoute("tournaments")
    data object Progress : AppRoute("progress")
    data object Analytics : AppRoute("analytics")
    data object Mastery : AppRoute("mastery")
    data object Goals : AppRoute("goals")
    data object StudyPlan : AppRoute("study-plan")
    data object Readiness : AppRoute("readiness")
    data object Focus : AppRoute("focus")
    data object Queue : AppRoute("queue")
    data object Milestones : AppRoute("milestones")
    data object Onboarding : AppRoute("onboarding")
    data object Tutor : AppRoute("tutor")
    data object Admin : AppRoute("admin")
    data object Settings : AppRoute("settings")
    data object Release : AppRoute("release")
}
