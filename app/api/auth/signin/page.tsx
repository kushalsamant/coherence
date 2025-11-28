"use client";

import { useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { signIn } from "next-auth/react";

function SignInContent() {
  const searchParams = useSearchParams();
  const app = searchParams.get("app");
  const returnUrl = searchParams.get("returnUrl") || searchParams.get("callbackUrl");

  useEffect(() => {
    // Redirect to Google OAuth with return URL
    const callbackUrl = returnUrl 
      ? `${returnUrl}?auth=success`
      : app 
        ? `https://${app}.kvshvl.in?auth=success`
        : "https://kvshvl.in?auth=success";

    signIn("google", {
      callbackUrl,
      redirect: true,
    });
  }, [app, returnUrl]);

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

