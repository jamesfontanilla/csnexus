package com.csnexus.app.core.design

import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import com.csnexus.app.R

/**
 * Display font family — Space Grotesk (Google Fonts, OFL licensed).
 * Used for headings, display text, and emphasis.
 * Fallback for Clash Display which requires a commercial license.
 */
val CSNexusDisplayFont = FontFamily(
    Font(R.font.space_grotesk_bold, FontWeight.Bold),
    Font(R.font.space_grotesk_semibold, FontWeight.SemiBold),
    Font(R.font.space_grotesk_medium, FontWeight.Medium),
)

/**
 * Body font family — DM Sans (Google Fonts, OFL licensed).
 * Used for body text, labels, and UI elements.
 * Fallback for Satoshi which requires a commercial license.
 */
val CSNexusBodyFont = FontFamily(
    Font(R.font.dm_sans_regular, FontWeight.Normal),
    Font(R.font.dm_sans_medium, FontWeight.Medium),
    Font(R.font.dm_sans_bold, FontWeight.Bold),
)
