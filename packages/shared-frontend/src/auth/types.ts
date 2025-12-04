/**
 * Authentication configuration types
 */

export interface AuthConfig {
  /** Application name (e.g., "ask", "reframe", "sketch2bim") */
  appName: string;
  /** Frontend URL environment variable name (e.g., "ASK_FRONTEND_URL") */
  frontendUrlEnvVar: string;
  /** Default frontend URL (e.g., "https://ask.kvshvl.in") */
  defaultFrontendUrl: string;
}

/**
 * Session user type
 */
export interface SessionUser {
  id: string;
  email: string;
  name?: string;
  image?: string;
}

/**
 * Session type returned by auth() function
 */
export interface Session {
  user: SessionUser;
  expires?: string;
}

