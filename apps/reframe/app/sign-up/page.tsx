"use client";

import { useState, useEffect, Suspense } from "react";
import { signIn, useSession } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";

function SignUpContent() {
  const [termsAccepted, setTermsAccepted] = useState(false);
  const [ageVerified, setAgeVerified] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();
  const searchParams = useSearchParams();
  const { data: session, status } = useSession();

  const canSubmit = termsAccepted && ageVerified && !isSubmitting;

  // Redirect authenticated users to home or callback URL
  useEffect(() => {
    if (status === "authenticated") {
      const callbackUrl = searchParams.get("callbackUrl") || "/";
      router.push(callbackUrl);
    }
  }, [status, router, searchParams]);

  const handleSignUp = async () => {
    if (!canSubmit) return;
    
    setIsSubmitting(true);
    try {
      // Store consent acceptance in sessionStorage to record after auth
      sessionStorage.setItem("pendingConsent", "true");
      
      await signIn("google", { callbackUrl: "/" });
    } catch (error) {
      console.error("Sign up error:", error);
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-b from-slate-50 to-slate-100">
      <Card className="w-full max-w-md shadow-lg">
        <CardContent className="p-8 space-y-6">
          {/* Header */}
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-bold">Join Reframe</h1>
            <p className="text-muted-foreground">
              Start reframing AI text with authentic human voices
            </p>
          </div>

          {/* Consent Checkboxes */}
          <div className="space-y-3 p-4 bg-slate-50 rounded-lg border border-slate-200">
            <div className="flex items-start space-x-3">
              <input
                type="checkbox"
                id="age-verification"
                checked={ageVerified}
                onChange={(e) => setAgeVerified(e.target.checked)}
                className="mt-1 w-4 h-4 rounded border-slate-300 text-primary focus:ring-primary cursor-pointer"
              />
              <label htmlFor="age-verification" className="text-sm cursor-pointer">
                I am at least 13 years old
              </label>
            </div>

            <div className="flex items-start space-x-3">
              <input
                type="checkbox"
                id="terms-acceptance"
                checked={termsAccepted}
                onChange={(e) => setTermsAccepted(e.target.checked)}
                className="mt-1 w-4 h-4 rounded border-slate-300 text-primary focus:ring-primary cursor-pointer"
              />
              <label htmlFor="terms-acceptance" className="text-sm cursor-pointer">
                I agree to the{" "}
                <a
                  href="/terms"
                  target="_blank"
                  className="text-primary underline hover:no-underline"
                  onClick={(e) => e.stopPropagation()}
                >
                  Terms of Service
                </a>{" "}
                and{" "}
                <a
                  href="/privacy"
                  target="_blank"
                  className="text-primary underline hover:no-underline"
                  onClick={(e) => e.stopPropagation()}
                >
                  Privacy Policy
                </a>
              </label>
            </div>
          </div>

          {/* OAuth Button */}
          <Button
            type="button"
            onClick={handleSignUp}
            disabled={!canSubmit}
            variant="outline"
            className="w-full h-12 text-base"
          >
            <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="currentColor"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="currentColor"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              />
              <path
                fill="currentColor"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
            </svg>
            Sign up with Google
          </Button>

          {/* Divider */}
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-200"></div>
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-white dark:bg-gray-900 px-2 text-slate-500 dark:text-slate-400">Secure Authentication</span>
            </div>
          </div>

          {/* Info Message */}
          {(!termsAccepted || !ageVerified) && !isSubmitting && (
            <div className="text-center text-sm text-amber-600 bg-amber-50 p-3 rounded-lg">
              Please accept both checkboxes above to continue
            </div>
          )}

          {/* Navigation Links */}
          <div className="text-center space-y-2">
            <div>
              <span className="text-sm text-muted-foreground">Already have an account? </span>
              <Link href="/sign-in" className="text-sm text-primary hover:underline font-medium">
                Sign in
              </Link>
            </div>
            <Link href="/" className="text-sm text-primary hover:underline block">
              ← Back to Home
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default function SignUpPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    }>
      <SignUpContent />
    </Suspense>
  );
}
