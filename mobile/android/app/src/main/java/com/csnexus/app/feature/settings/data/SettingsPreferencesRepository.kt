package com.csnexus.app.feature.settings.data

import android.content.Context
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import com.csnexus.app.core.datastore.appPreferencesDataStore
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

data class SettingsPreferences(
    val dailyGoalMinutes: Int = 30,
    val defaultQuizMode: String = "practice",
    val examDate: String = "",
    val reducedMotion: String = "system",
    val fontSize: String = "default",
    val theme: String = "system",
    val notificationsEnabled: Boolean = true,
    val soundEnabled: Boolean = true,
    val hapticEnabled: Boolean = true,
)

class SettingsPreferencesRepository(
    private val context: Context,
) {
    suspend fun read(): SettingsPreferences {
        return observe().first()
    }

    fun observe(): Flow<SettingsPreferences> {
        return context.appPreferencesDataStore.data.map { preferences ->
            SettingsPreferences(
                dailyGoalMinutes = preferences[Keys.DAILY_GOAL_MINUTES] ?: 30,
                defaultQuizMode = preferences[Keys.DEFAULT_QUIZ_MODE] ?: "practice",
                examDate = preferences[Keys.EXAM_DATE] ?: "",
                reducedMotion = preferences[Keys.REDUCED_MOTION] ?: "system",
                fontSize = preferences[Keys.FONT_SIZE] ?: "default",
                theme = preferences[Keys.THEME] ?: "system",
                notificationsEnabled = preferences[Keys.NOTIFICATIONS_ENABLED] ?: true,
                soundEnabled = preferences[Keys.SOUND_ENABLED] ?: true,
                hapticEnabled = preferences[Keys.HAPTIC_ENABLED] ?: true,
            )
        }
    }

    suspend fun save(preferences: SettingsPreferences) {
        context.appPreferencesDataStore.edit { store ->
            store[Keys.DAILY_GOAL_MINUTES] = preferences.dailyGoalMinutes.coerceIn(5, 180)
            store[Keys.DEFAULT_QUIZ_MODE] = preferences.defaultQuizMode
            store[Keys.EXAM_DATE] = preferences.examDate
            store[Keys.REDUCED_MOTION] = preferences.reducedMotion
            store[Keys.FONT_SIZE] = preferences.fontSize
            store[Keys.THEME] = preferences.theme
            store[Keys.NOTIFICATIONS_ENABLED] = preferences.notificationsEnabled
            store[Keys.SOUND_ENABLED] = preferences.soundEnabled
            store[Keys.HAPTIC_ENABLED] = preferences.hapticEnabled
        }
    }

    private object Keys {
        val DAILY_GOAL_MINUTES = intPreferencesKey("settings_daily_goal_minutes")
        val DEFAULT_QUIZ_MODE = stringPreferencesKey("settings_default_quiz_mode")
        val EXAM_DATE = stringPreferencesKey("settings_exam_date")
        val REDUCED_MOTION = stringPreferencesKey("settings_reduced_motion")
        val FONT_SIZE = stringPreferencesKey("settings_font_size")
        val THEME = stringPreferencesKey("settings_theme")
        val NOTIFICATIONS_ENABLED = booleanPreferencesKey("settings_notifications_enabled")
        val SOUND_ENABLED = booleanPreferencesKey("settings_sound_enabled")
        val HAPTIC_ENABLED = booleanPreferencesKey("settings_haptic_enabled")
    }
}
