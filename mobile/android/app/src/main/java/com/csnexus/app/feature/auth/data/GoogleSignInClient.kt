package com.csnexus.app.feature.auth.data

import android.content.Context
import android.util.Base64
import android.util.Log
import androidx.credentials.CredentialManager
import androidx.credentials.CustomCredential
import androidx.credentials.GetCredentialRequest
import androidx.credentials.exceptions.GetCredentialException
import androidx.credentials.exceptions.NoCredentialException
import com.google.android.libraries.identity.googleid.GetGoogleIdOption
import com.google.android.libraries.identity.googleid.GetSignInWithGoogleOption
import com.google.android.libraries.identity.googleid.GoogleIdTokenCredential
import com.google.android.libraries.identity.googleid.GoogleIdTokenParsingException
import java.security.SecureRandom

class GoogleSignInClient(
    context: Context,
    private val serverClientId: String,
) {
    private val credentialManager = CredentialManager.create(context)
    private val credentialContext = context

    suspend fun signInWithBottomSheet(): String? {
        return try {
            requestIdToken(filterAuthorizedAccounts = true, useButtonOption = false)
                ?: requestIdToken(filterAuthorizedAccounts = false, useButtonOption = false)
        } catch (_: NoCredentialException) {
            requestIdToken(filterAuthorizedAccounts = false, useButtonOption = false)
        } catch (_: GetCredentialException) {
            null
        }
    }

    suspend fun signInWithGoogleButton(): GoogleSignInResult {
        return try {
            requestIdToken(filterAuthorizedAccounts = false, useButtonOption = true)
                ?.let(GoogleSignInResult::Success)
                ?: requestStandardIdToken(previousFailure = "button_empty_token")
        } catch (error: GetCredentialException) {
            Log.w(TAG, "Google button sign-in failed: ${error.diagnosticType()}", error)
            requestStandardIdToken(previousFailure = "button_${error.diagnosticType()}")
        }
    }

    private suspend fun requestIdToken(
        filterAuthorizedAccounts: Boolean,
        useButtonOption: Boolean,
    ): String? {
        val request = GetCredentialRequest.Builder()
            .addCredentialOption(
                if (useButtonOption) {
                    GetSignInWithGoogleOption.Builder(serverClientId = serverClientId)
                        .setNonce(generateSecureRandomNonce())
                        .build()
                } else {
                    GetGoogleIdOption.Builder()
                        .setFilterByAuthorizedAccounts(filterAuthorizedAccounts)
                        .setAutoSelectEnabled(filterAuthorizedAccounts)
                        .setServerClientId(serverClientId)
                        .setNonce(generateSecureRandomNonce())
                        .build()
                },
            )
            .build()

        val response = credentialManager.getCredential(
            request = request,
            context = credentialContext,
        )
        val credential = response.credential
        if (credential is CustomCredential &&
            credential.type == GoogleIdTokenCredential.TYPE_GOOGLE_ID_TOKEN_CREDENTIAL
        ) {
            return try {
                GoogleIdTokenCredential.createFrom(credential.data).idToken
            } catch (error: GoogleIdTokenParsingException) {
                Log.w(TAG, "Google ID token parsing failed", error)
                null
            }
        }
        Log.w(TAG, "Unsupported Google credential returned: ${credential::class.java.name}")
        return null
    }

    private suspend fun requestStandardIdToken(previousFailure: String): GoogleSignInResult {
        return try {
            requestIdToken(filterAuthorizedAccounts = false, useButtonOption = false)
                ?.let(GoogleSignInResult::Success)
                ?: GoogleSignInResult.Failure(
                    userMessage = "Google did not return a usable sign-in token. Please try again.",
                    diagnostic = "$previousFailure;standard_empty_token",
                )
        } catch (error: NoCredentialException) {
            Log.w(TAG, "No Google credential available after $previousFailure: ${error.diagnosticType()}", error)
            GoogleSignInResult.Failure(
                userMessage = "Google could not find an eligible account for this app. Confirm the Android OAuth package and SHA fingerprints match this APK, then try again.",
                diagnostic = "$previousFailure;standard_${error.diagnosticType()}",
            )
        } catch (error: GetCredentialException) {
            Log.w(TAG, "Google credential request failed after $previousFailure: ${error.diagnosticType()}", error)
            GoogleSignInResult.Failure(
                userMessage = "Google sign-in could not continue. Make sure this APK's SHA fingerprint is registered in Google Cloud and try again.",
                diagnostic = "$previousFailure;standard_${error.diagnosticType()}",
            )
        }
    }
}

private fun generateSecureRandomNonce(byteLength: Int = 32): String {
    val randomBytes = ByteArray(byteLength)
    SecureRandom().nextBytes(randomBytes)
    return Base64.encodeToString(randomBytes, Base64.NO_WRAP or Base64.URL_SAFE or Base64.NO_PADDING)
}

private const val TAG = "GoogleSignInClient"

private fun GetCredentialException.diagnosticType(): String {
    return type.ifBlank { this::class.java.simpleName }
}

sealed interface GoogleSignInResult {
    data class Success(val idToken: String) : GoogleSignInResult
    data class Failure(
        val userMessage: String,
        val diagnostic: String,
    ) : GoogleSignInResult
}
