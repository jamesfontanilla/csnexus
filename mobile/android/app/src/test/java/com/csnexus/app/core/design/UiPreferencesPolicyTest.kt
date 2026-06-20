package com.csnexus.app.core.design

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class UiPreferencesPolicyTest {
    @Test
    fun resolveDarkThemeAlwaysReturnsDark() {
        // Dark-only enforcement per task 12.1 — app always renders dark regardless of preference.
        assertTrue(resolveDarkTheme(themePreference = "light", systemIsDark = true))
        assertTrue(resolveDarkTheme(themePreference = "dark", systemIsDark = false))
        assertTrue(resolveDarkTheme(themePreference = "system", systemIsDark = false))
    }

    @Test
    fun fontScaleMultiplierMapsSupportedDisplaySizes() {
        assertEquals(0.875f, fontScaleMultiplier("compact"), 0.0001f)
        assertEquals(1f, fontScaleMultiplier("default"), 0.0001f)
        assertEquals(1.15f, fontScaleMultiplier("large"), 0.0001f)
    }

    @Test
    fun reducedMotionPreferenceOverridesSystemOnlyWhenRequested() {
        assertTrue(resolveReducedMotionPreference("on", systemReducedMotion = false))
        assertFalse(resolveReducedMotionPreference("off", systemReducedMotion = true))
        assertTrue(resolveReducedMotionPreference("system", systemReducedMotion = true))
        assertFalse(resolveReducedMotionPreference("system", systemReducedMotion = false))
    }
}
