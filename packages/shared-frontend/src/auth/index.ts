/**
 * Shared Auth Package
 * Centralized Authentication - Redirects to main site (kvshvl.in) for authentication
 * All OAuth flows are handled at kvshvl.in/api/auth/callback/google
 */
import { redirect } from "next/navigation";
import type { AuthConfig, Session } from "./types";

/**
 * Get the auth URL (main site URL for authentication)
 */
function getAuthUrl(): string {
  return (
    process.env.NEXT_PUBLIC_AUTH_URL ||
    (process.env.NODE_ENV === "development" ? "http://localhost:3000" : "https://kvshvl.in")
  );
}

/**
 * Get the current app's frontend URL
 */
function getFrontendUrl(config: AuthConfig): string {
  if (typeof window !== "undefined") {
    return window.location.href;
  }
  return process.env[config.frontendUrlEnvVar] || config.defaultFrontendUrl;
}

/**
 * Create authentication functions for an app
 * 
 * @param config - Authentication configuration
 * @returns Object with signIn, signOut, auth, and handlers functions
 */
export function createAuthFunctions(config: AuthConfig) {
  const { appName } = config;

  async function signIn() {
    const authUrl = getAuthUrl();
    const currentUrl = getFrontendUrl(config);
    // Redirect directly to Google OAuth endpoint, bypassing intermediate signin page
    redirect(`${authUrl}/api/auth/signin/google?app=${appName}&returnUrl=${encodeURIComponent(currentUrl)}`);
  }

  async function signOut() {
    const authUrl = getAuthUrl();
    redirect(`${authUrl}/api/auth/signout`);
  }

  async function auth(): Promise<Session | null> {
    // For apps, we'll handle session validation via API calls to main site
    // or use JWT tokens passed from main site after auth
    // TODO: Implement proper session validation
    return null;
  }

  const handlers = {
    GET: async () => {
      redirect(`${getAuthUrl()}/api/auth/signin/google?app=${appName}`);
    },
    POST: async () => {
      redirect(`${getAuthUrl()}/api/auth/signin/google?app=${appName}`);
    },
  };

  return {
    signIn,
    signOut,
    auth,
    handlers,
  };
}

/**
 * Export types
 */
export type { AuthConfig, Session, SessionUser } from "./types";
