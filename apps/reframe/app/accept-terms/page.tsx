"use client";

import { useState, useEffect } from "react";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useToast } from "@/components/ui/use-toast";

export default function AcceptTermsPage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const { toast } = useToast();

  const [termsAccepted, setTermsAccepted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const isLoaded = status !== "loading";
  const isSignedIn = !!session?.user;

  // Redirect if not signed in
  useEffect(() => {
    if (isLoaded && !isSignedIn) {
      router.push("/sign-in");
    }
  }, [isLoaded, isSignedIn, router]);

  const handleAccept = async () => {
    if (!termsAccepted || isSubmitting) return;

    setIsSubmitting(true);
    try {
      const response = await fetch("/api/consent/record", {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Failed to record consent");
      }

      toast({
        title: "Terms Accepted",
        description: "Thank you for accepting our updated Terms and Privacy Policy.",
      });

      // Redirect to home
      router.push("/");
    } catch (error) {
      console.error("Error accepting terms:", error);
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to record acceptance. Please try again.",
      });
      setIsSubmitting(false);
    }
  };

  if (!isLoaded || !isSignedIn) {
    return <div className="p-8 text-center">Loading...</div>;
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-b from-slate-50 to-slate-100">
      <Card className="w-full max-w-2xl shadow-lg">
        <CardContent className="p-8 space-y-6">
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-bold">Accept Updated Terms</h1>
            <p className="text-slate-600">
              We&apos;ve updated our Terms of Service and Privacy Policy. Please review and accept to continue using Reframe.
            </p>
          </div>

          <div className="bg-slate-50 border border-slate-200 rounded-lg p-6 space-y-4">
            <h2 className="text-xl font-semibold">What&apos;s New</h2>
            <ul className="list-disc pl-6 space-y-2 text-sm text-slate-700">
              <li>Enhanced data privacy protections and GDPR compliance</li>
              <li>Clear consent tracking with timestamps</li>
              <li>Self-service data export and account deletion</li>
              <li>Updated third-party service information</li>
              <li>Improved transparency about data handling</li>
            </ul>
          </div>

          <div className="space-y-4">
            <div className="flex gap-4">
              <Button variant="outline" asChild className="flex-1">
                <a href="/terms" target="_blank">
                  Read Terms of Service
                </a>
              </Button>
              <Button variant="outline" asChild className="flex-1">
                <a href="/privacy" target="_blank">
                  Read Privacy Policy
                </a>
              </Button>
            </div>

            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  id="terms-acceptance"
                  checked={termsAccepted}
                  onChange={(e) => setTermsAccepted(e.target.checked)}
                  className="mt-1 w-4 h-4 rounded border-slate-300 text-primary focus:ring-primary cursor-pointer"
                />
                <label htmlFor="terms-acceptance" className="text-sm cursor-pointer">
                  I have read and agree to the updated{" "}
                  <a
                    href="/terms"
                    target="_blank"
                    className="text-primary underline hover:no-underline"
                  >
                    Terms of Service
                  </a>{" "}
                  and{" "}
                  <a
                    href="/privacy"
                    target="_blank"
                    className="text-primary underline hover:no-underline"
                  >
                    Privacy Policy
                  </a>
                </label>
              </div>
            </div>

            <Button
              onClick={handleAccept}
              disabled={!termsAccepted || isSubmitting}
              className="w-full"
            >
              {isSubmitting ? "Processing..." : "Accept and Continue"}
            </Button>

            <p className="text-xs text-center text-slate-500">
              You must accept the updated terms to continue using Reframe
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

