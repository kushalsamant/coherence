/**
 * API Client for Reframe FastAPI Backend
 * Uses Next.js API proxy route to add JWT authentication
 */
export interface ReframeRequest {
  text: string;
  tone?: "conversational" | "professional" | "academic" | "enthusiastic" | "empathetic" | "witty";
  generation?: "any" | "silent" | "boomers" | "genx" | "millennials" | "genz" | "genalpha" | "genbeta" | "kids";
  timezoneOffset?: number;
}

export interface ReframeResponse {
  output: string;
  usage?: number;
}

export interface ReframeError {
  error: string;
  usage?: number;
}

/**
 * Reframe text using FastAPI backend via Next.js proxy
 * The proxy route handles JWT token authentication
 */
export async function reframeText(request: ReframeRequest): Promise<ReframeResponse> {
  // Use the Next.js proxy route which handles JWT authentication
  const response = await fetch("/api/reframe-proxy", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text: request.text,
      tone: request.tone || "conversational",
      generation: request.generation || "any",
      timezoneOffset: request.timezoneOffset || 0,
    }),
    credentials: "include", // Include cookies for session
  });

  if (!response.ok) {
    const errorData: ReframeError = await response.json().catch(() => ({
      error: `HTTP ${response.status}: ${response.statusText}`,
    }));
    throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
  }

  const data: ReframeResponse = await response.json();
  return data;
}

