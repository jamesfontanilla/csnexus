package com.csnexus.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.zIndex
import com.csnexus.app.core.design.AmbientBackground
import com.csnexus.app.core.design.CSNexusTheme
import com.csnexus.app.core.design.LocalCSNexusPerformanceTier
import com.csnexus.app.core.design.detectPerformanceTier
import com.csnexus.app.core.design.performanceTierOverride
import com.csnexus.app.core.navigation.CSNexusNavGraph
import com.csnexus.app.feature.settings.data.SettingsPreferences

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val app = application as CsnexusApplication
        setContent {
            val performanceTier = remember {
                performanceTierOverride(intent.getStringExtra("performance_tier"))
                    ?: detectPerformanceTier(this@MainActivity)
            }
            val preferences by app.container.settingsPreferencesRepository
                .observe()
                .collectAsState(initial = SettingsPreferences())
            CSNexusTheme(
                themePreference = preferences.theme,
                fontSizePreference = preferences.fontSize,
                reducedMotionPreference = preferences.reducedMotion,
            ) {
                CompositionLocalProvider(LocalCSNexusPerformanceTier provides performanceTier) {
                    Box(modifier = Modifier.fillMaxSize()) {
                        AmbientBackground(modifier = Modifier.zIndex(-1f))
                        CSNexusNavGraph(container = app.container)
                    }
                }
            }
        }
    }
}
