"use client";

import { useSearchParams } from "next/navigation";
import { Suspense } from "react";
import Link from "next/link";
import { Button } from "@kushalsamant/design-template";

function ErrorContent() {
  const searchParams = useSearchParams();
  const error = searchParams.get("error");
  
  // Get all URL parameters for debugging
  const allParams: Record<string, string | null> = {};
  if (typeof window !== "undefined") {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.forEach((value, key) => {
      allParams[key] = value;
    });
  }

  // Map error codes to user-friendly messages
  const errorMessages: Record<string, string> = {
    Configuration: "There is a problem with the server configuration. Check that GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and AUTH_SECRET are set correctly.",
    AccessDenied: "You do not have permission to sign in.",
    Verification: "The verification token has expired or has already been used.",
    OAuthSignin: "Error in constructing an authorization URL.",
    OAuthCallback: "Error in handling the response from an OAuth provider.",
    OAuthCreateAccount: "Could not create OAuth account in the provider.",
    EmailCreateAccount: "Could not create email account.",
    Callback: "Error in the OAuth callback handler route.",
    OAuthAccountNotLinked: "Email on the account is already linked, but not with this OAuth account.",
    EmailSignin: "Sending the e-mail with the sign in token failed.",
    CredentialsSignin: "The authorize callback returned null in the Credentials provider.",
    SessionRequired: "The content of this page requires you to be signed in at all times.",
    Default: "An error occurred during authentication. Please try again.",
  };

  const errorMessage = errorMessages[error || ""] || errorMessages.Default;
  const errorCode = error || "Unknown";

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        padding: "var(--space-xl)",
        fontFamily: "Times New Roman, serif",
        textAlign: "center",
      }}
    >
      <h1 style={{ fontSize: "var(--font-size-3xl)", marginBottom: "var(--space-md)" }}>
        Authentication Error
      </h1>
      <p style={{ fontSize: "var(--font-size-lg)", marginBottom: "var(--space-sm)", color: "var(--color-text-secondary)" }}>
        Error Code: {errorCode}
      </p>
      <p style={{ fontSize: "var(--font-size-base)", marginBottom: "var(--space-xl)", maxWidth: "600px" }}>
        {errorMessage}
      </p>
      <div style={{ display: "flex", gap: "var(--space-md)", flexWrap: "wrap", justifyContent: "center" }}>
        <Link href="/api/auth/signin">
          <Button variant="primary">Try Again</Button>
        </Link>
        <Link href="/">
          <Button variant="secondary">Go Home</Button>
        </Link>
      </div>
      {(process.env.NODE_ENV === "development" || !error) && (
        <details style={{ marginTop: "var(--space-xl)", textAlign: "left", maxWidth: "800px" }}>
          <summary style={{ cursor: "pointer", marginBottom: "var(--space-sm)" }}>
            Debug Information
          </summary>
          <pre
            style={{
              padding: "var(--space-md)",
              backgroundColor: "var(--color-bg-secondary)",
              borderRadius: "var(--radius-md)",
              overflow: "auto",
              fontSize: "var(--font-size-sm)",
            }}
          >
            {JSON.stringify(
              {
                error: errorCode,
                allUrlParams: allParams,
                timestamp: new Date().toISOString(),
                url: typeof window !== "undefined" ? window.location.href : "",
                referrer: typeof window !== "undefined" ? document.referrer : "",
              },
              null,
              2
            )}
          </pre>
        </details>
      )}
    </div>
  );
}

export default function AuthErrorPage() {
  return (
    <Suspense
      fallback={
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            minHeight: "100vh",
            fontFamily: "Times New Roman, serif",
          }}
        >
          <p>Loading...</p>
        </div>
      }
    >
      <ErrorContent />
    </Suspense>
  );
}
