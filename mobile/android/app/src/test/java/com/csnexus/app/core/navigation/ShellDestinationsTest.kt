package com.csnexus.app.core.navigation

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class ShellDestinationsTest {
    @Test
    fun filterShellDestinationsReturnsAllItemsForBlankQuery() {
        val results = filterShellDestinations("", shellDestinations)

        assertEquals(shellDestinations.size, results.size)
    }

    @Test
    fun filterShellDestinationsMatchesLabelsAndKeywords() {
        val analyticsResults = filterShellDestinations("stats", shellDestinations)
        val moduleResults = filterShellDestinations("subjects", shellDestinations)

        assertTrue(analyticsResults.any { it.route == AppRoute.Progress })
        assertTrue(moduleResults.any { it.route == AppRoute.Modules })
    }

    @Test
    fun filterShellDestinationsDoesNotLeakAdminWhenCallerExcludesIt() {
        val nonAdminDestinations = shellDestinations.filter { !it.adminOnly }
        val results = filterShellDestinations("admin", nonAdminDestinations)

        assertFalse(results.any { it.route == AppRoute.Admin })
    }
}
