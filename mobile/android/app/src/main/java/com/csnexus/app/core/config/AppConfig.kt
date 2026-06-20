package com.csnexus.app.core.config

import com.csnexus.app.BuildConfig

data class AppConfig(
    val apiBaseUrl: String,
    val googleServerClientId: String,
)

fun appConfig(): AppConfig = AppConfig(
    apiBaseUrl = BuildConfig.API_BASE_URL,
    googleServerClientId = BuildConfig.GOOGLE_SERVER_CLIENT_ID,
)
