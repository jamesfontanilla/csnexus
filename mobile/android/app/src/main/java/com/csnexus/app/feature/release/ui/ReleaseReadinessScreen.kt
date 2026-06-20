package com.csnexus.app.feature.release.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun ReleaseReadinessScreen(contentPadding: PaddingValues) {
    Column(
        modifier = Modifier.fillMaxSize().padding(contentPadding).padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        Text("Release Readiness", style = MaterialTheme.typography.headlineMedium)
        Text("Debug and Android-test artifacts are built and ready for device install.")
        Text("Quality gate: unit tests, debug build, Android test build, release build, and targeted emulator instrumentation have been executed.")
        Text("Signing: configure keystore.properties or CI secrets before shipping a signed production artifact.")
        Text("Backend gaps still block final full-parity certification for refresh-token auth, Google sign-in configuration, and some sync contracts.")
        Text("Capacitor wrapper: keep until native feature parity is accepted in production.")
    }
}
