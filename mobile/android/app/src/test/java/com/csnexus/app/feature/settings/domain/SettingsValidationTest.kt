package com.csnexus.app.feature.settings.domain

import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class SettingsValidationTest {
    @Test
    fun passwordRequiresWebPolicyRules() {
        assertTrue(isValidPassword("Password1!"))
        assertFalse(isValidPassword("short1!"))
        assertFalse(isValidPassword("password1!"))
        assertFalse(isValidPassword("PASSWORD1!"))
        assertFalse(isValidPassword("Password!"))
        assertFalse(isValidPassword("Password1"))
    }

    @Test
    fun goalRangesMatchSettingsControls() {
        assertTrue(isValidDailyGoalMinutes(5))
        assertTrue(isValidDailyGoalMinutes(180))
        assertFalse(isValidDailyGoalMinutes(4))
        assertFalse(isValidDailyGoalMinutes(181))

        assertTrue(isValidDailyGoalXp(10))
        assertTrue(isValidDailyGoalXp(500))
        assertFalse(isValidDailyGoalXp(9))
        assertFalse(isValidDailyGoalXp(501))
    }
}
