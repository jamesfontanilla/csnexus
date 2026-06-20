package com.csnexus.app.core.datastore

import android.content.Context
import androidx.datastore.preferences.preferencesDataStore

val Context.appPreferencesDataStore by preferencesDataStore(name = "app_preferences")
val Context.sessionDataStore by preferencesDataStore(name = "session")
