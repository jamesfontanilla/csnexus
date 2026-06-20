# Android App

CSNexus uses Capacitor to package the existing React/Vite frontend as a native Android app. The FastAPI backend and production database stay hosted remotely, so lessons, questions, user progress, and server-side features keep using the same source of truth as the web app.

## First-Time Setup

1. Install Android Studio and the Android SDK.
2. Copy `.env.android.example` to `.env.android`.
3. Set `VITE_API_URL` in `.env.android` to the deployed FastAPI HTTPS URL.
4. Run:

```powershell
npm run android:sync
npm run android:open
```

Android Studio will open `web/android`. From there, run the app on an emulator/device or create a signed Play Store build.

## Updating Lessons Or Features

Backend and database updates are deployed exactly as they are for the web app. If a lesson, quiz bank, or feature is served by the API, Android users receive it without rebuilding the Android app.

Frontend updates still need a new Android build because the React bundle is packaged into the app:

```powershell
npm run android:sync
```

Then rebuild from Android Studio or CI.

## Notes

- The Android app should use an absolute `VITE_API_URL` for custom deployments, but the shipped build now falls back to `https://api.csnexus.space` when the env var is omitted.
- Keep native-only features in Capacitor plugins or Android code under `web/android`.
- Google sign-in may need an Android OAuth client or native plugin before Play Store release, depending on how the WebView handles the current web sign-in flow.
