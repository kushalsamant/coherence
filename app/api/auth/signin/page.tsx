"use client";

import { useEffect, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth-provider";

function SignInContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { signIn } = useAuth();
  const app = searchParams.get("app");
  const returnUrl = searchParams.get("returnUrl") || searchParams.get("callbackUrl");

  useEffect(() => {
    const handleSignIn = async () => {
      // Get the base URL from the current origin (works for both localhost and production)
      const baseUrl = typeof window !== "undefined" ? window.location.origin : "http://localhost:3000";
      
      // Determine the default callback URL based on environment
      let defaultCallbackUrl: string;
      if (returnUrl) {
        // If returnUrl is provided, use it (preserve existing query params if any)
        defaultCallbackUrl = returnUrl.includes("?") 
          ? `${returnUrl}&auth=success` 
          : `${returnUrl}?auth=success`;
      } else if (app) {
        // For subdomain apps, use the app's URL
        defaultCallbackUrl = `https://${app}.kvshvl.in?auth=success`;
      } else {
        // Default: redirect to account page on current origin (localhost or production)
        defaultCallbackUrl = `${baseUrl}/account`;
      }

      // Store the callback URL in sessionStorage for after OAuth redirect
      if (typeof window !== "undefined") {
        sessionStorage.setItem("auth_callback_url", defaultCallbackUrl);
      }

      await signIn("google");
    };

    handleSignIn();
  }, [app, returnUrl, signIn]);

  return (
    <div style={{ 
      display: "flex", 
      justifyContent: "center", 
      alignItems: "center", 
      minHeight: "100vh",
      fontFamily: "Times New Roman, serif"
    }}>
      <p>Redirecting to Google Sign In...</p>
    </div>
  );
}

export default function SignInPage() {
  return (
    <Suspense fallback={
      <div style={{ 
        display: "flex", 
        justifyContent: "center", 
        alignItems: "center", 
        minHeight: "100vh",
        fontFamily: "Times New Roman, serif"
      }}>
        <p>Loading...</p>
      </div>
    }>
      <SignInContent />
    </Suspense>
  );
}
