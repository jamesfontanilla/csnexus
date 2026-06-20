package com.csnexus.app.core.design

import android.app.ActivityManager
import android.content.Context
import android.os.Build
import androidx.compose.runtime.staticCompositionLocalOf

/**
 * Device performance tier used to gate expensive visual effects.
 * - High: All effects enabled (blur, ambient blobs, animations)
 * - Medium: No blur effects, but keep animations and ambient blobs
 * - Low: No blur, no ambient blobs — solid backgrounds only
 */
enum class PerformanceTier {
    High,
    Medium,
    Low;

    val blurEnabled: Boolean get() = this == High
    val ambientBlobsEnabled: Boolean get() = this != Low
    val animationsEnabled: Boolean get() = this != Low
}

val LocalCSNexusPerformanceTier = staticCompositionLocalOf { PerformanceTier.High }

/**
 * Detects the device performance tier at startup.
 * Heuristics:
 * - Low: <4GB RAM or <4 CPU cores or SDK < 26
 * - Medium: 4-6GB RAM or SDK < 31 (no RenderEffect)
 * - High: 6GB+ RAM and SDK >= 31 and 6+ cores
 */
fun detectPerformanceTier(context: Context): PerformanceTier {
    val activityManager = context.getSystemService(Context.ACTIVITY_SERVICE) as ActivityManager
    val memInfo = ActivityManager.MemoryInfo()
    activityManager.getMemoryInfo(memInfo)
    val totalRamGb = memInfo.totalMem / (1024L * 1024L * 1024L)
    val cpuCores = Runtime.getRuntime().availableProcessors()
    val sdk = Build.VERSION.SDK_INT
    val isEmulator = Build.FINGERPRINT.contains("generic", ignoreCase = true) ||
        Build.FINGERPRINT.contains("emulator", ignoreCase = true) ||
        Build.MODEL.contains("sdk", ignoreCase = true) ||
        Build.MODEL.contains("emulator", ignoreCase = true)

    return when {
        isEmulator -> PerformanceTier.Low
        totalRamGb < 4 || cpuCores < 4 || sdk < 26 -> PerformanceTier.Low
        totalRamGb < 6 || sdk < 31 -> PerformanceTier.Medium
        else -> PerformanceTier.High
    }
}

fun performanceTierOverride(value: String?): PerformanceTier? {
    return when (value?.lowercase()) {
        "low" -> PerformanceTier.Low
        "medium" -> PerformanceTier.Medium
        "high" -> PerformanceTier.High
        else -> null
    }
}
