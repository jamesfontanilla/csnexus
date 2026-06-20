package com.csnexus.app.core.network

import com.csnexus.app.core.auth.SessionManager
import com.csnexus.app.core.logging.AppLogger
import com.csnexus.app.core.logging.NoOpAppLogger
import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import retrofit2.Retrofit

class ApiClientFactory(
    private val baseUrl: String,
    private val authInterceptor: AuthInterceptor,
    private val sessionManager: SessionManager? = null,
    private val logger: AppLogger = NoOpAppLogger,
) {
    private val json = Json {
        ignoreUnknownKeys = true
        explicitNulls = false
    }

    private val client: OkHttpClient = OkHttpClient.Builder()
        .addInterceptor(DiagnosticsInterceptor(logger))
        .addInterceptor(authInterceptor)
        .apply {
            sessionManager?.let { authenticator(SessionAuthenticator(it)) }
        }
        .build()

    private val retrofit: Retrofit = Retrofit.Builder()
        .baseUrl(baseUrl)
        .client(client)
        .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
        .build()

    fun <T> create(service: Class<T>): T = retrofit.create(service)
}
