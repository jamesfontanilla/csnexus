package com.csnexus.app.core.design

import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.widthIn
import androidx.compose.ui.Modifier
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.dp

fun Modifier.csnexusMinimumTouchTarget(): Modifier =
    this
        .heightIn(min = CSNexusAccessibility.MinTouchTarget)
        .widthIn(min = CSNexusAccessibility.MinTouchTarget)

fun Modifier.csnexusHeading(): Modifier = semantics { heading() }

fun Modifier.csnexusRole(role: Role): Modifier = semantics { this.role = role }

fun Modifier.csnexusContentDescription(label: String): Modifier =
    semantics { contentDescription = label }

object CSNexusAccessibility {
    val MinTouchTarget = 48.dp
    val CompactTouchTarget = 44.dp
}
