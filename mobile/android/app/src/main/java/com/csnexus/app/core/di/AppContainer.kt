package com.csnexus.app.core.di

import android.content.Context
import androidx.work.WorkManager
import com.csnexus.app.core.auth.AuthRepository
import com.csnexus.app.core.auth.EncryptedTokenStore
import com.csnexus.app.core.auth.SessionManager
import com.csnexus.app.core.config.appConfig
import com.csnexus.app.core.database.AppDatabase
import com.csnexus.app.core.logging.AndroidAppLogger
import com.csnexus.app.core.logging.AppLogger
import com.csnexus.app.core.network.ApiClientFactory
import com.csnexus.app.core.network.AuthInterceptor
import com.csnexus.app.core.sync.OfflineSyncProcessor
import com.csnexus.app.core.sync.OfflineSyncScheduler
import com.csnexus.app.core.sync.OfflineSyncStore
import com.csnexus.app.core.sync.buildSyncProcessor
import com.csnexus.app.feature.auth.data.AuthApi
import com.csnexus.app.feature.content.data.ContentApi
import com.csnexus.app.feature.content.data.ContentRepository
import com.csnexus.app.feature.content.data.RoomLessonCache
import com.csnexus.app.feature.flashcards.data.FlashcardCacheStore
import com.csnexus.app.feature.flashcards.data.FlashcardApi
import com.csnexus.app.feature.flashcards.data.FlashcardRepository
import com.csnexus.app.feature.leaderboards.data.LeaderboardApi
import com.csnexus.app.feature.leaderboards.data.LeaderboardRepository
import com.csnexus.app.feature.mockexam.data.MockExamApi
import com.csnexus.app.feature.mockexam.data.MockExamRepository
import com.csnexus.app.feature.mockexam.data.RoomMockExamReviewCache
import com.csnexus.app.feature.motivation.data.OfflineSyncFocusQueueStore
import com.csnexus.app.feature.motivation.data.MotivationApi
import com.csnexus.app.feature.motivation.data.MotivationRepository
import com.csnexus.app.feature.motivation.data.SharedPreferencesMotivationStore
import com.csnexus.app.feature.progress.data.ProgressCacheStore
import com.csnexus.app.feature.progress.data.ProgressApi
import com.csnexus.app.feature.progress.data.ProgressRepository
import com.csnexus.app.feature.quizzes.data.QuizApi
import com.csnexus.app.feature.quizzes.data.QuizRepository
import com.csnexus.app.feature.quizzes.data.SharedPreferencesActiveQuizStore
import com.csnexus.app.feature.settings.data.SettingsApi
import com.csnexus.app.feature.settings.data.SettingsPreferencesRepository
import com.csnexus.app.feature.settings.data.SettingsRepository
import com.csnexus.app.feature.admin.data.AdminApi
import com.csnexus.app.feature.admin.data.AdminRepository
import com.csnexus.app.feature.tutor.data.TutorApi
import com.csnexus.app.feature.tutor.data.TutorRepository

class AppContainer(context: Context) {
    private val appContext = context.applicationContext
    private val config = appConfig()
    val googleServerClientId: String = config.googleServerClientId
    val logger: AppLogger = AndroidAppLogger()
    private val appDatabase: AppDatabase by lazy {
        AppDatabase.get(appContext)
    }
    private val syncPair: Pair<OfflineSyncStore, OfflineSyncProcessor> by lazy {
        buildSyncProcessor(appContext, appDatabase.syncEventDao(), logger)
    }
    val offlineSyncStore: OfflineSyncStore by lazy { syncPair.first }
    val offlineSyncProcessor: OfflineSyncProcessor by lazy { syncPair.second }
    val offlineSyncScheduler: OfflineSyncScheduler by lazy {
        OfflineSyncScheduler(WorkManager.getInstance(appContext))
    }
    val tokenStore: EncryptedTokenStore by lazy { EncryptedTokenStore(appContext) }
    val sessionManager: SessionManager by lazy { SessionManager({ tokenStore }, logger) }
    private val apiFactory: ApiClientFactory by lazy {
        ApiClientFactory(
        baseUrl = config.apiBaseUrl,
        authInterceptor = AuthInterceptor(tokenStore),
        sessionManager = sessionManager,
        logger = logger,
        )
    }
    private val authApi: AuthApi by lazy {
        apiFactory.create(AuthApi::class.java).also(sessionManager::bindAuthApi)
    }

    val authRepository: AuthRepository by lazy { AuthRepository(
        authApi = authApi,
        tokenStore = tokenStore,
        sessionManager = sessionManager,
        logger = logger,
    ) }

    val contentRepository: ContentRepository by lazy { ContentRepository(
        contentApi = apiFactory.create(ContentApi::class.java),
        lessonCache = RoomLessonCache(
            contentCacheDao = appDatabase.contentCacheDao(),
            lessonCacheDao = appDatabase.lessonCacheDao(),
        ),
        syncStore = offlineSyncStore,
        syncScheduler = offlineSyncScheduler,
    ) }

    val quizRepository: QuizRepository by lazy { QuizRepository(
        quizApi = apiFactory.create(QuizApi::class.java),
        activeQuizStore = SharedPreferencesActiveQuizStore(appContext),
    ) }

    val mockExamRepository: MockExamRepository by lazy { MockExamRepository(
        mockExamApi = apiFactory.create(MockExamApi::class.java),
        reviewCache = RoomMockExamReviewCache(appDatabase.finalizedReviewDao()),
    ) }

    val progressRepository: ProgressRepository by lazy { ProgressRepository(
        progressApi = apiFactory.create(ProgressApi::class.java),
        cacheStore = ProgressCacheStore(appDatabase.progressSnapshotDao()),
        syncStore = offlineSyncStore,
        syncScheduler = offlineSyncScheduler,
        syncProcessor = offlineSyncProcessor,
    ) }

    private val motivationStore: SharedPreferencesMotivationStore by lazy {
        SharedPreferencesMotivationStore(appContext)
    }

    val motivationRepository: MotivationRepository by lazy { MotivationRepository(
        motivationApi = apiFactory.create(MotivationApi::class.java),
        onboardingStore = motivationStore,
        focusStateStore = motivationStore,
        focusCompletionQueueStore = OfflineSyncFocusQueueStore(offlineSyncStore),
        syncStore = offlineSyncStore,
        syncScheduler = offlineSyncScheduler,
        syncProcessor = offlineSyncProcessor,
    ) }

    val settingsPreferencesRepository: SettingsPreferencesRepository by lazy {
        SettingsPreferencesRepository(appContext)
    }

    val settingsRepository: SettingsRepository by lazy { SettingsRepository(
        settingsApi = apiFactory.create(SettingsApi::class.java),
        preferencesRepository = settingsPreferencesRepository,
        syncStore = offlineSyncStore,
        syncScheduler = offlineSyncScheduler,
        syncProcessor = offlineSyncProcessor,
    ) }

    val flashcardRepository: FlashcardRepository by lazy { FlashcardRepository(
        flashcardApi = apiFactory.create(FlashcardApi::class.java),
        cacheStore = FlashcardCacheStore(appDatabase.flashcardCacheDao()),
        offlineSyncStore = offlineSyncStore,
        syncScheduler = offlineSyncScheduler,
        syncProcessor = offlineSyncProcessor,
    ) }

    val leaderboardRepository: LeaderboardRepository by lazy { LeaderboardRepository(
        leaderboardApi = apiFactory.create(LeaderboardApi::class.java),
    ) }

    val tutorRepository: TutorRepository by lazy { TutorRepository(
        tutorApi = apiFactory.create(TutorApi::class.java),
    ) }

    val adminRepository: AdminRepository by lazy { AdminRepository(
        adminApi = apiFactory.create(AdminApi::class.java),
    ) }
}
