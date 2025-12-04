"use client";

import { useState, useEffect } from "react";
import { useSession, signOut } from "@/lib/auth-provider";
import { useRouter } from "next/navigation";
import { Button } from "@/components/reframe/ui/button";
import { Card, CardContent } from "@/components/reframe/ui/card";
import { useToast } from "@/components/reframe/ui/use-toast";
import { DeleteAccountModal } from "@/components/reframe/delete-account-modal";
import { ExportDataModal } from "@/components/reframe/export-data-modal";
import Link from "next/link";
import type { UserMetadata } from "@/lib/reframe/user-metadata";
import type { ConsentRecord } from "@/lib/reframe/consent";
import { logger } from "@/lib/logger";

export default function SettingsPage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const { toast } = useToast();

  const [metadata, setMetadata] = useState<UserMetadata | null>(null);
  const [consent, setConsent] = useState<ConsentRecord | null>(null);
  const [usage, setUsage] = useState(0);
  const [hasActiveSubscription, setHasActiveSubscription] = useState(false);
  const [loading, setLoading] = useState(true);
  
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showExportModal, setShowExportModal] = useState(false);

  const isLoaded = status !== "loading";
  const isSignedIn = !!session?.user;
  const user = session?.user;

  // Redirect if not signed in
  useEffect(() => {
    if (isLoaded && !isSignedIn) {
      router.push("/sign-in");
    }
  }, [isLoaded, isSignedIn, router]);

  // Fetch user data
  useEffect(() => {
    const fetchData = async () => {
      if (!isSignedIn || !user?.id) return;

      try {
        // Fetch metadata
        const metadataRes = await fetch("/api/user-metadata");
        const metadataData = await metadataRes.json();
        setMetadata(metadataData);

        // Fetch actual usage from Redis (includes subscription status)
        const timezoneOffset = new Date().getTimezoneOffset();
        const usageRes = await fetch(`/api/usage?userId=${user.id}&timezoneOffset=${timezoneOffset}`);
        const usageData = await usageRes.json();
        if (usageData.usage !== undefined) {
          setUsage(usageData.usage);
        }
        if (usageData.hasActiveSubscription !== undefined) {
          setHasActiveSubscription(usageData.hasActiveSubscription);
        }

        // Fetch consent (we'll need to create an API for this or include in metadata)
        try {
          const consentRes = await fetch("/api/consent/get");
          if (consentRes.ok) {
            const consentData = await consentRes.json();
            setConsent(consentData);
          }
        } catch (e) {
          logger.info("No consent data available");
        }

        setLoading(false);
      } catch (error) {
        logger.error("Error fetching user data:", error);
        setLoading(false);
      }
    };

    fetchData();
  }, [isSignedIn, user?.id]);

  const handleExportData = () => {
    setShowExportModal(true);
  };

  const handleDeleteAccount = async () => {
    try {
      const response = await fetch("/api/account/delete", {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Failed to delete account");
      }

      toast({
        title: "Account Deleted",
        description: "Your account has been permanently deleted.",
      });

      // Sign out and redirect
      await signOut({ redirect: false });
      router.push("/");
    } catch (error) {
      logger.error("Delete error:", error);
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to delete account. Please try again.",
      });
    }
  };

  const handleManageSubscription = async () => {
    try {
      // Razorpay subscription management - redirect to pricing page
      window.location.href = "/pricing";
    } catch (error) {
      logger.error("Portal error:", error);
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to open subscription portal.",
      });
    }
  };

  const getSubscriptionDisplay = () => {
    const tier = metadata?.subscription_tier || metadata?.subscription;
    if (!tier || tier === "trial") return "Free / Trial";
    if (tier === "monthly") return "Monthly Pro";
    if (tier === "yearly") return "Yearly Pro";
    return "Free";
  };

  const getUserUsageDisplay = () => {
    const tier = metadata?.subscription_tier || metadata?.subscription;
    const isPro = tier === "monthly" || tier === "yearly";
    const isTrial = tier === "trial";

    if (hasActiveSubscription && isPro) {
      return "Unlimited (Pro)";
    }
    if (isTrial && hasActiveSubscription) {
      return "Unlimited (Trial)";
    }
    return `${usage}/5 used (free tier)`;
  };

  if (!isLoaded || !isSignedIn) {
    return <div className="p-8 text-center">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 p-4 py-12">
      <div className="container mx-auto max-w-4xl space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">Account Settings</h1>
            <p className="text-slate-600 mt-1">Manage your account and preferences</p>
          </div>
          <Button variant="outline" asChild>
            <Link href="/">← Back to Home</Link>
          </Button>
        </div>

        {/* Account Overview Card */}
        <Card>
          <CardContent className="p-6 space-y-4">
            <h2 className="text-xl font-semibold">Account Overview</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-slate-600">Email</p>
                <p className="font-medium">{user?.email}</p>
              </div>
              <div>
                <p className="text-sm text-slate-600">User ID</p>
                <p className="font-mono text-sm">{user?.id?.slice(0, 16)}...</p>
              </div>
              <div>
                <p className="text-sm text-slate-600">Current Plan</p>
                <p className="font-medium">{getSubscriptionDisplay()}</p>
                {metadata?.subscription_expires_at && (
                  <p className="text-xs text-slate-500 mt-1">
                    Expires: {new Date(metadata.subscription_expires_at).toLocaleDateString()}
                  </p>
                )}
              </div>
              {consent && (
                <div>
                  <p className="text-sm text-slate-600">Terms Accepted</p>
                  <p className="font-medium">
                    {new Date(consent.acceptedAt).toLocaleDateString()}
                  </p>
                </div>
              )}
            </div>
            <div className="pt-4 border-t border-slate-200">
              <Button variant="outline" onClick={() => signOut({ callbackUrl: "/" })}>
                Sign Out
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Usage Statistics Card */}
        <Card>
          <CardContent className="p-6 space-y-4">
            <h2 className="text-xl font-semibold">Usage & Subscription</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-slate-600">Current Usage</p>
                <p className="font-medium">{getUserUsageDisplay()}</p>
              </div>
              {metadata?.subscription_status && (
                <div>
                  <p className="text-sm text-slate-600">Status</p>
                  <p className="font-medium capitalize">{metadata.subscription_status}</p>
                </div>
              )}
            </div>
            {!hasActiveSubscription && (
              <Button asChild>
                <a href="/pricing">Upgrade to Pro</a>
              </Button>
            )}
          </CardContent>
        </Card>

        {/* Subscription Management Card */}
        {(hasActiveSubscription || metadata?.subscription_tier) && metadata?.subscription_tier !== "trial" && (
          <Card>
            <CardContent className="p-6 space-y-4">
              <h2 className="text-xl font-semibold">Subscription Management</h2>
              <p className="text-slate-600">
                {metadata?.subscription_auto_renew 
                  ? "Your subscription is set to auto-renew. Cancel anytime before your next billing cycle."
                  : "Your subscription will not auto-renew. Resume to continue after expiration."}
              </p>
              <div className="flex gap-3">
                <Button onClick={handleManageSubscription} variant="outline">
                  Go to Pricing Page
                </Button>
                {metadata?.razorpay_subscription_id && (
                  <>
                    {metadata?.subscription_auto_renew ? (
                      <Button 
                        onClick={async () => {
                          try {
                            const res = await fetch("/api/razorpay/subscriptions/cancel", { method: "POST" });
                            const data = await res.json();
                            if (data.status === "success") {
                              toast({ title: "Subscription cancelled", description: data.message });
                              // Refresh metadata
                              window.location.reload();
                            }
                          } catch (error) {
                            toast({ variant: "destructive", title: "Error", description: "Failed to cancel subscription" });
                          }
                        }}
                        variant="destructive"
                      >
                        Cancel Subscription
                      </Button>
                    ) : (
                      <Button 
                        onClick={async () => {
                          try {
                            const res = await fetch("/api/razorpay/subscriptions/resume", { method: "POST" });
                            const data = await res.json();
                            if (data.status === "success") {
                              toast({ title: "Subscription resumed", description: data.message });
                              // Refresh metadata
                              window.location.reload();
                            }
                          } catch (error) {
                            toast({ variant: "destructive", title: "Error", description: "Failed to resume subscription" });
                          }
                        }}
                      >
                        Resume Subscription
                      </Button>
                    )}
                  </>
                )}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Data & Privacy Card */}
        <Card>
          <CardContent className="p-6 space-y-4">
            <h2 className="text-xl font-semibold">Data & Privacy</h2>
            <p className="text-slate-600">
              You have full control over your personal data in compliance with GDPR and CCPA regulations.
            </p>
            <div className="space-y-3">
              <div className="flex items-start space-x-3 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex-1">
                  <h3 className="font-semibold text-blue-900">Export Your Data</h3>
                  <p className="text-sm text-blue-700 mt-1">
                    Download a complete copy of your personal data in JSON format (GDPR Right to Access).
                  </p>
                </div>
                <Button variant="outline" size="sm" onClick={handleExportData}>
                  Export Data
                </Button>
              </div>

              <div className="flex items-start space-x-3 p-4 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex-1">
                  <h3 className="font-semibold text-red-900">Delete Account</h3>
                  <p className="text-sm text-red-700 mt-1">
                    Permanently delete your account and all associated data (GDPR Right to Erasure). This action cannot be undone.
                  </p>
                </div>
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={() => setShowDeleteModal(true)}
                >
                  Delete Account
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Legal Documents Card */}
        <Card>
          <CardContent className="p-6 space-y-4">
            <h2 className="text-xl font-semibold">Legal Documents</h2>
            <div className="flex flex-wrap gap-3">
              <Button variant="outline" asChild>
                <a href="/terms" target="_blank">
                  Terms of Service
                </a>
              </Button>
              <Button variant="outline" asChild>
                <a href="/privacy" target="_blank">
                  Privacy Policy
                </a>
              </Button>
            </div>
            {consent && (
              <p className="text-sm text-slate-600">
                You accepted Terms v{consent.termsVersion} and Privacy v{consent.privacyVersion} on{" "}
                {new Date(consent.acceptedAt).toLocaleString()}
              </p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Modals */}
      <DeleteAccountModal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        onConfirm={handleDeleteAccount}
      />
      <ExportDataModal
        isOpen={showExportModal}
        onClose={() => setShowExportModal(false)}
        userId={user?.id || ""}
      />
    </div>
  );
}

