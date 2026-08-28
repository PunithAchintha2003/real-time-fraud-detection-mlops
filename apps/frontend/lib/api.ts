const API_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:4000";

type RefreshResponse = {
  accessToken: string;
};

export async function refreshAccessToken(): Promise<string | null> {
  try {
    const response = await fetch(`${API_URL}/auth/refresh`, {
      method: "POST",
      credentials: "include",
    });

    if (!response.ok) {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("user");
      return null;
    }

    const data = (await response.json()) as RefreshResponse;

    localStorage.setItem("accessToken", data.accessToken);

    return data.accessToken;
  } catch {
    return null;
  }
}

export async function authFetch(
  input: string,
  init: RequestInit = {},
): Promise<Response> {
  let accessToken = localStorage.getItem("accessToken");

  const createHeaders = (token: string | null) => {
    const headers = new Headers(init.headers);

    if (token) {
      headers.set("Authorization", `Bearer ${token}`);
    }

    return headers;
  };

  let response = await fetch(input, {
    ...init,
    credentials: "include",
    headers: createHeaders(accessToken),
  });

  if (response.status !== 401) {
    return response;
  }

  accessToken = await refreshAccessToken();

  if (!accessToken) {
    return response;
  }

  response = await fetch(input, {
    ...init,
    credentials: "include",
    headers: createHeaders(accessToken),
  });

  return response;
}

export async function logout() {
  try {
    await fetch(`${API_URL}/auth/logout`, {
      method: "POST",
      credentials: "include",
    });
  } finally {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("user");
  }
}