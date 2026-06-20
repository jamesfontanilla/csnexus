package com.csnexus.app.feature.settings.data

import com.csnexus.app.core.network.ApiResult
import com.csnexus.app.core.network.safeApiCall
import com.csnexus.app.core.sync.OfflineSyncProcessor
import com.csnexus.app.core.sync.OfflineSyncScheduler
import com.csnexus.app.core.sync.OfflineSyncStore
import com.csnexus.app.core.sync.SettingsDailyGoalSyncPayload
import com.csnexus.app.core.sync.SyncBannerState
import com.csnexus.app.core.sync.SyncEventType
import com.csnexus.app.core.sync.SyncFeature
import java.io.IOException
import kotlinx.coroutines.flow.Flow

class SettingsRepository(
    private val settingsApi: SettingsApi,
    private val preferencesRepository: SettingsPreferencesRepository,
    private val syncStore: OfflineSyncStore? = null,
    private val syncScheduler: OfflineSyncScheduler? = null,
    private val syncProcessor: OfflineSyncProcessor? = null,
) {
    suspend fun readPreferences(): SettingsPreferences = preferencesRepository.read()

    fun observePreferences(): Flow<SettingsPreferences> = preferencesRepository.observe()

    suspend fun saveLocalPreferences(preferences: SettingsPreferences) {
        preferencesRepository.save(preferences)
    }

    fun syncBanner(): Flow<SyncBannerState?>? = syncStore?.observe(SyncFeature.Settings)

    suspend fun saveDailyGoal(targetXp: Int): ApiResult<DailyGoalResponseDto> {
        val clampedTarget = targetXp.coerceIn(10, 500)
        return try {
            ApiResult.Success(settingsApi.updateDailyGoal(DailyGoalRequestDto(clampedTarget)))
        } catch (error: IOException) {
            if (syncStore == null) {
                ApiResult.Failure(com.csnexus.app.core.error.AppError.Network(error.message ?: "Network unavailable"))
            } else {
                syncStore.enqueue(
                    SyncEventType.SettingsDailyGoalUpdate,
                    SettingsDailyGoalSyncPayload(targetXp = clampedTarget),
                )
                syncScheduler?.schedule()
                ApiResult.Success(DailyGoalResponseDto(targetXp = clampedTarget, status = "queued_offline"))
            }
        } catch (error: RuntimeException) {
            ApiResult.Failure(com.csnexus.app.core.error.AppError.Unknown(error.message ?: "Unknown error"))
        }
    }

    suspend fun retrySync(): ApiResult<Int> {
        val processor = syncProcessor ?: return ApiResult.Success(0)
        syncScheduler?.schedule()
        return ApiResult.Success(processor.process(SyncFeature.Settings).synced)
    }
}
