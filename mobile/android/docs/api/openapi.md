# Backend API Contract

The Android app consumes the existing FastAPI `/v1/*` API. Contract refresh should be automated once the backend is running locally.

Recommended local export flow:

```powershell
# Terminal 1, repo root
uvicorn app.main:app --reload

# Terminal 2
Invoke-WebRequest http://127.0.0.1:8000/openapi.json -OutFile mobile/android/docs/api/openapi.json
```

High-priority Android DTOs should be checked against:

- `POST /v1/auth/sessions`
- `POST /v1/auth/sessions:refresh`
- `GET /v1/auth/me`
- `DELETE /v1/auth/sessions/me`
- `GET /v1/modules`
- `GET /v1/modules/{module_id}/topics`
- `GET /v1/topics/{topic_id}/subtopics`
- `GET /v1/subtopics/{subtopic_id}/lesson`

If backend schemas change incompatibly, Android API mapper and repository tests should fail before release.
