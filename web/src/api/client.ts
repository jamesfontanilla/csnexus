import { getToken, logout } from "../stores/auth";

export interface ErrorResponse {
  error: {
    message: string;
    code: string;
  };
}

export class ApiError extends Error {
  status: number;
  code: string;
  requestId: string | null;

  constructor(status: number, message: string, code: string, requestId: string | null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.requestId = requestId;
  }
}

const API_BASE = import.meta.env.VITE_API_URL || "";

async function request<T>(method: string, url: string, body?: unknown): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${url}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  const requestId = response.headers.get("X-Request-ID");

  if (!response.ok) {
    let errorBody: unknown = null;
    try {
      errorBody = await response.json();
    } catch {
      // response may not be JSON
    }

    // Auto-logout on 401 — token is stale/invalid (e.g., after server restart)
    if (response.status === 401) {
      logout();
      // Use replace so the back button doesn't loop back to the broken page
      window.location.replace("/login");
    }

    // Extract error message from various response shapes
    let message = `Request failed with status ${response.status}`;
    let code = "UNKNOWN";

    if (errorBody && typeof errorBody === "object") {
      const body = errorBody as Record<string, unknown>;
      // Shape 1: {"error": {"message": "...", "code": "..."}}
      if (body.error && typeof body.error === "object") {
        const err = body.error as Record<string, unknown>;
        if (err.message) message = String(err.message);
        if (err.code) code = String(err.code);
      }
      // Shape 2: FastAPI 422 {"detail": [{"msg": "...", "loc": [...]}]}
      else if (Array.isArray(body.detail)) {
        const messages = (body.detail as Array<{ msg?: string; loc?: string[] }>)
          .map((d) => d.msg || "Validation error")
          .join("; ");
        message = messages;
        code = "VALIDATION_ERROR";
      }
      // Shape 3: {"detail": "some string"}
      else if (typeof body.detail === "string") {
        message = body.detail;
        code = `HTTP_${response.status}`;
      }
    }

    throw new ApiError(response.status, message, code, requestId);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

export const apiClient = {
  get<T>(url: string): Promise<T> {
    return request<T>("GET", url);
  },

  post<T>(url: string, body?: unknown): Promise<T> {
    return request<T>("POST", url, body);
  },

  put<T>(url: string, body?: unknown): Promise<T> {
    return request<T>("PUT", url, body);
  },

  patch<T>(url: string, body?: unknown): Promise<T> {
    return request<T>("PATCH", url, body);
  },

  delete<T>(url: string): Promise<T> {
    return request<T>("DELETE", url);
  },
};
