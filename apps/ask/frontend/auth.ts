import { redirect } from "next/navigation";

/**
 * Centralized Authentication - Redirects to main site (kvshvl.in) for authentication
 * All OAuth flows are handled at kvshvl.in/api/auth/callback/google
 */
export async function signIn() {
  const authUrl = process.env.NEXT_PUBLIC_AUTH_URL || 
                  (process.env.NODE_ENV === "development" 
                    ? "http://localhost:3000" 
                    : "https://kvshvl.in");
  const currentUrl = typeof window !== "undefined" 
    ? window.location.href 
    : process.env.ASK_FRONTEND_URL || "https://ask.kvshvl.in";
  
  redirect(`${authUrl}/api/auth/signin?app=ask&returnUrl=${encodeURIComponent(currentUrl)}`);
}

export async function signOut() {
  const authUrl = process.env.NEXT_PUBLIC_AUTH_URL || 
                  (process.env.NODE_ENV === "development" 
                    ? "http://localhost:3000" 
                    : "https://kvshvl.in");
  
  redirect(`${authUrl}/api/auth/signout`);
}

export async function auth() {
  // For apps, we'll handle session validation via API calls to main site
  // or use JWT tokens passed from main site after auth
  return null;
}

// Export handlers for API routes (if needed for compatibility)
export const handlers = {
  GET: async () => {
    redirect(`${process.env.NEXT_PUBLIC_AUTH_URL || "https://kvshvl.in"}/api/auth/signin?app=ask`);
  },
  POST: async () => {
    redirect(`${process.env.NEXT_PUBLIC_AUTH_URL || "https://kvshvl.in"}/api/auth/signin?app=ask`);
  },
};

