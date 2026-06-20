package com.csnexus.app.core.auth

interface TokenStore {
    fun accessToken(): String?
    fun refreshToken(): String?
    fun saveAccessToken(token: String) = saveTokens(token, refreshToken())
    fun saveTokens(accessToken: String, refreshToken: String?)
    fun clear()
    fun isAuthenticated(): Boolean = !accessToken().isNullOrBlank()
}
