/**
 * Centralized Authentication - Redirects to main site (kvshvl.in) for authentication
 * All OAuth flows are handled at kvshvl.in/api/auth/callback/google
 */
import { createAuthFunctions } from "@kvshvl/shared-frontend/auth";

const auth = createAuthFunctions({
  appName: "ask",
  frontendUrlEnvVar: "ASK_FRONTEND_URL",
  defaultFrontendUrl: "https://ask.kvshvl.in",
});

export const { signIn, signOut, auth: authFunction, handlers } = auth;
