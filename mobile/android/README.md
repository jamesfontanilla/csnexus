# CSNexus Native Android

This is the full native Android client for CSNexus. It is separate from the React web app in `web/` and separate from the Capacitor WebView wrapper in `web/android`.

## Stack

- Kotlin
- Jetpack Compose
- Material 3
- Gradle Kotlin DSL
- Retrofit/OkHttp
- Kotlinx Serialization
- Room/DataStore
- Encrypted Android token storage

## Folder

```text
mobile/android
```

Native Android source belongs here. Do not put native rewrite code under `web/android`; that folder is only the Capacitor wrapper.

## API Configuration

The Android app talks to the existing FastAPI backend. Base URLs are configured in `app/build.gradle.kts`:

- `debug`: `http://10.0.2.2:8000/`
- `staging`: placeholder staging HTTPS URL
- `release`: placeholder production HTTPS URL

Replace staging/release placeholders before publishing.

## Local Setup

Install:

1. Android Studio
2. JDK 17, or Android Studio's bundled JBR
3. Android SDK 36
4. A local `local.properties` file based on `local.properties.example`

Then run:

```powershell
cd mobile/android
.\gradlew.bat test
.\gradlew.bat assembleDebug
```

This machine is configured with Android Studio's bundled JBR and Android SDK under `C:\Users\Jaime\AppData\Local\Android\Sdk`.

## Milestone 1 Scope

| Area | Status |
| --- | --- |
| Project scaffold | Partial |
| Build config | Partial |
| Native theme/navigation shell | Partial |
| Email/password login | Partial |
| Content module list | Partial |
| Lesson reader | Planned |
| Quiz flow | Planned |
| Dashboard/profile/progress | Placeholder |

## Release Notes

Signing keys must stay out of git. Add release signing through local `keystore.properties` or CI secrets before producing Play Store builds.
