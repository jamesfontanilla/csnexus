# Native Android Release Notes

## Build Commands

```powershell
cd mobile/android
.\gradlew.bat testDebugUnitTest
.\gradlew.bat assembleDebug
.\gradlew.bat assembleDebugAndroidTest
.\gradlew.bat assembleRelease
```

## Device Testing

Debug APK:

- `app/build/outputs/apk/debug/app-debug.apk`

Android test APK:

- `app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk`

Install and run on a connected emulator/device:

```powershell
adb install -r app/build/outputs/apk/debug/app-debug.apk
adb install -r app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk
adb shell am instrument -w -e class com.csnexus.app.feature.content.ui.LessonRendererScreenTest com.csnexus.app.debug.test/androidx.test.runner.AndroidJUnitRunner
```

## Signing

Do not commit signing keys. Use one of:

- local `keystore.properties` ignored by git
- CI secrets
- Android Studio generated signing configuration for local release testing

Recommended local keys:

```properties
storeFile=C\:\\path\\to\\csnexus-release.jks
storePassword=...
keyAlias=csnexus
keyPassword=...
```

## Observability

Production diagnostics selection is documented in [diagnostics-tooling.md](/C:/Users/Jaime/Documents/GitHub/csnexus/mobile/android/docs/diagnostics-tooling.md).

Current decision:

- Firebase Crashlytics for crash reporting
- Firebase Analytics for release-approved product analytics only
- in-app `AppLogger` as the redacting abstraction in front of any provider

## Readiness Report

Current certification evidence and remaining release boundaries are summarized in [release-readiness-report.md](/C:/Users/Jaime/Documents/GitHub/csnexus/mobile/android/docs/release-readiness-report.md).

## Capacitor Wrapper

Keep `web/android` as the temporary Android WebView wrapper until the native app reaches accepted feature parity.
