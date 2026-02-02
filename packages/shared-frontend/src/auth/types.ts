/**
 * Authentication configuration types
 */

export interface AuthConfig {
  /** Application name (e.g., "sketch2bim") */
  appName: string;
  /** Frontend URL environment variable name (e.g., "SKETCH2BIM_FRONTEND_URL") */
  frontendUrlEnvVar: string;
  /** Default frontend URL (e.g., "https://sketch2bim.kvshvl.in") */
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

