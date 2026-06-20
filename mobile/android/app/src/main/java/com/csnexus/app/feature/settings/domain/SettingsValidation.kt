package com.csnexus.app.feature.settings.domain

const val DELETE_ACCOUNT_CONFIRMATION = "DELETE MY ACCOUNT"

fun isValidPassword(value: String): Boolean {
    return value.length >= 8 &&
        value.any(Char::isUpperCase) &&
        value.any(Char::isLowerCase) &&
        value.any(Char::isDigit) &&
        value.any { !it.isLetterOrDigit() && !it.isWhitespace() }
}

fun isValidDailyGoalXp(value: Int): Boolean = value in 10..500

fun isValidDailyGoalMinutes(value: Int): Boolean = value in 5..180
