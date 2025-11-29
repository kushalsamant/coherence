"use client";

import { useState, useEffect, Suspense } from "react";
import { useSession, signOut } from "next-auth/react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { useToast } from "@/components/ui/use-toast";
import { TONES, GENERATIONS, type ToneName, type GenerationId } from "@/lib/tones";
import { toErrorWithMessage } from "@/types";

type CharacterLimit = {
  name: string;
  limit: number;
  cost: string;
  description: string;
  proOnly: boolean;
};

// Fixed character limit: 10,000 words (~50,000 characters) for all users
const CHARACTER_LIMIT = 50000;

function HomeContent() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const searchParams = useSearchParams();
  const { toast } = useToast();

  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [usage, setUsage] = useState(0);
  const [loading, setLoading] = useState(false);
  const [selectedTone, setSelectedTone] = useState<ToneName>("conversational");
  const [selectedGeneration, setSelectedGeneration] = useState<GenerationId>("any");
  const [subscriptionTier, setSubscriptionTier] = useState<string | undefined>(undefined);
  const [hasActiveSubscription, setHasActiveSubscription] = useState(false);

  const isLoaded = status !== "loading";
  const isSignedIn = !!session?.user;
  const user = session?.user;
  const isPro = subscriptionTier === "monthly" || subscriptionTier === "yearly";
  const isFreeLimit = !hasActiveSubscription && usage >= 5;
  
  const getUserPlanDisplay = () => {
    if (!subscriptionTier || subscriptionTier === "trial") return "Free / Trial";
    if (subscriptionTier === "monthly") return "Monthly Pro";
    if (subscriptionTier === "yearly") return "Yearly Pro";
    return "Free";
  };
  
  const getUserUsageDisplay = () => {
    if (hasActiveSubscription && (isPro || subscriptionTier === "trial")) {
      return "Unlimited";
    }
    return `${usage}/5 used (free tier)`;
  };

  // Fetch user metadata and usage on mount
  useEffect(() => {
    const fetchUserData = async () => {
      if (!isSignedIn || !user?.id) return;
      try {
        // Fetch metadata (subscription)
        const metadataRes = await fetch('/api/user-metadata');
        const metadataData = await metadataRes.json();
        const tier = metadataData.subscription_tier || metadataData.subscription;
        if (tier) {
          setSubscriptionTier(tier);
        }

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
      } catch (error) {
        console.error("Failed to fetch user data:", error);
      }
    };
    fetchUserData();
  }, [isSignedIn, user?.id]);

  // Show success toast after payment redirect
  useEffect(() => {
    const successParam = searchParams.get("success");
    const checkoutParam = searchParams.get("checkout");
    
    if (successParam === "true" || checkoutParam === "success") {
      toast({ title: "Upgrade successful!", description: "Unlimited access unlocked." });
    }
  }, [searchParams, toast]);

  // Record consent after successful sign-in
  useEffect(() => {
    const recordConsentIfNeeded = async () => {
      if (!isSignedIn || !user?.id) return;
      
      const pendingConsent = sessionStorage.getItem("pendingConsent");
      if (pendingConsent === "true") {
        try {
          await fetch("/api/consent/record", { method: "POST" });
          sessionStorage.removeItem("pendingConsent");
        } catch (error) {
          console.error("Failed to record consent:", error);
        }
      }
    };
    
    recordConsentIfNeeded();
  }, [isSignedIn, user?.id]);

  const handleSubmit = async () => {
    if (!isSignedIn) return router.push('/sign-in');
    if (input.trim().length < 10) return toast({ variant: "destructive", title: "Too short", description: "Enter at least 10 characters." });

    setLoading(true);
    try {
      // Use the proxy route which forwards to FastAPI backend
      const res = await fetch("/api/reframe-proxy", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          text: input, 
          tone: selectedTone,
          generation: selectedGeneration,
          timezoneOffset: new Date().getTimezoneOffset() // Minutes from UTC
        }),
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setOutput(data.output);
      if (data.usage !== undefined) {
        setUsage(data.usage);
      }
      
      const toneName = TONES.find(t => t.id === selectedTone)?.name || selectedTone;
      toast({ title: `Reframed in ${toneName} tone!`, description: data.output.slice(0, 100) + "..." });
    } catch (error) {
      const err = toErrorWithMessage(error);
      // Don't show error toast for limit errors - banner already visible
      if (!err.message.includes("limit reached")) {
        toast({ variant: "destructive", title: "Error", description: err.message });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleToneSelect = (toneId: ToneName) => {
    const tone = TONES.find(t => t.id === toneId);
    if (tone?.premium && !hasActiveSubscription) {
      toast({
        title: "Premium Tone!",
        description: "Upgrade to unlock Enthusiastic, Empathetic, and Witty tones.",
        action: (
          <Button size="sm" asChild variant="default" className="px-4">
            <a href="/pricing">View Plans</a>
          </Button>
        ),
      });
      return;
    }
    setSelectedTone(toneId);
  };

  const getCharCountColor = () => {
    const percentage = (input.length / CHARACTER_LIMIT) * 100;
    if (percentage < 50) return "text-green-600";
    if (percentage < 80) return "text-yellow-600";
    return "text-orange-600";
  };

  const copyOutput = () => {
    navigator.clipboard.writeText(output);
    toast({ description: "Copied to clipboard!" });
  };

  if (!isLoaded) return <div className="p-8">Loading...</div>;

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-b from-slate-50 to-slate-100">
      <Card className="w-full max-w-3xl shadow-lg">
        <CardContent className="p-8 space-y-8">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <Link href="/">
                <h1 className="text-3xl font-bold text-center cursor-pointer hover:text-primary transition-colors">Reframe</h1>
              </Link>
              <p className="text-center text-muted-foreground">Reframe text with authentic human voices</p>
            </div>
          </div>

          {!isSignedIn ? (
            <Button className="w-full" onClick={() => router.push('/sign-in')}>
              Sign Up Free
            </Button>
          ) : (
            <>
              {isFreeLimit && (
                <div className="bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-400 rounded-lg p-6 text-center space-y-3 shadow-md">
                  <div className="flex items-center justify-center gap-2">
                    <span className="text-2xl">🎯</span>
                    <div className="text-amber-900 font-bold text-lg">
                      Free Trial Complete (5/5)
                    </div>
                  </div>
                  <p className="text-amber-800 text-sm">
                    You&apos;ve used all 5 free requests. Upgrade for unlimited access!
                  </p>
                  <Button asChild size="lg" className="bg-primary hover:bg-primary/90 font-semibold">
                    <a href="/pricing">
                      View Plans & Pricing →
                    </a>
                  </Button>
                </div>
              )}

              {/* Tone Selector */}
              <div className="space-y-4">
                  <label className="text-sm font-medium">Choose Your Tone:</label>
                  <div className="grid grid-cols-1 gap-4">
                    {TONES.map((tone) => {
                      const isLocked = tone.premium && !hasActiveSubscription;
                      const isSelected = selectedTone === tone.id;
                      return (
                        <div key={tone.id} className="relative group">
                          <button
                            onClick={() => handleToneSelect(tone.id)}
                            className={`
                              relative p-3 rounded-lg border-2 text-left transition-all w-full
                              ${isSelected ? "border-primary bg-primary/5" : "border-slate-200 hover:border-slate-300"}
                              ${isLocked ? "opacity-60 cursor-not-allowed" : "cursor-pointer"}
                            `}
                            title={tone.description}
                          >
                            {isLocked && (
                              <div className="absolute top-2 right-2 text-sm">🔒</div>
                            )}
                            <div className="space-y-1">
                              <div className="flex items-center gap-2">
                                <input
                                  type="radio"
                                  checked={isSelected}
                                  readOnly
                                  className="w-3 h-3"
                                />
                                <span className="text-lg">{tone.icon}</span>
                                <span className="font-semibold text-sm">{tone.name}</span>
                              </div>
                              <div className="text-xs text-slate-500 ml-5">
                                {tone.description}
                              </div>
                            </div>
                          </button>
                          
                          {/* Hover Tooltip with Before/After Examples */}
                          <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-80 p-4 bg-white dark:bg-gray-800 border-2 border-slate-300 dark:border-gray-700 rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50 pointer-events-none hidden md:block">
                            <div className="space-y-3">
                              <div className="text-xs font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide">Preview</div>
                              <div className="space-y-2">
                                <div>
                                  <div className="text-xs font-medium text-red-600 dark:text-red-400 mb-1">Before:</div>
                                  <div className="text-xs text-slate-700 dark:text-slate-300 italic">&quot;{tone.example.before}&quot;</div>
                                </div>
                                <div>
                                  <div className="text-xs font-medium text-green-600 dark:text-green-400 mb-1">After ({tone.name}):</div>
                                  <div className="text-xs text-slate-700 dark:text-slate-300 italic">&quot;{tone.example.after}&quot;</div>
                                </div>
                              </div>
                            </div>
                            {/* Arrow pointing down */}
                            <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-1">
                              <div className="w-3 h-3 bg-white dark:bg-gray-800 border-r-2 border-b-2 border-slate-300 dark:border-gray-700 transform rotate-45"></div>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

              {/* Generation/Audience Selector */}
              <div className="space-y-4">
                <label className="text-sm font-medium">Target Generation (Optional):</label>
                <select
                  value={selectedGeneration}
                  onChange={(e) => setSelectedGeneration(e.target.value as GenerationId)}
                  className="w-full p-3 border-2 border-slate-200 rounded-lg focus:border-primary focus:outline-none"
                >
                  {GENERATIONS.map((gen) => (
                    <option key={gen.id} value={gen.id}>
                      {gen.name} {gen.years && `(${gen.years})`}
                    </option>
                  ))}
                </select>
                <p className="text-xs text-slate-500">
                  Adapt language and references for your target audience
                </p>
              </div>

              {/* Usage Stats Card */}
              <div className="bg-slate-100 dark:bg-gray-800 rounded-lg p-5 space-y-3">
                <div className="flex justify-between items-center">
                  <div className="text-sm text-muted-foreground">
                    <strong>Usage:</strong> {getUserUsageDisplay()}
                  </div>
                  {!hasActiveSubscription && (
                    <Button size="sm" variant="outline" asChild>
                      <a href="/pricing">View Plans</a>
                    </Button>
                  )}
                </div>
                <div className={`text-sm font-medium ${getCharCountColor()}`}>
                  <strong>Characters:</strong> {input.length.toLocaleString()} / {CHARACTER_LIMIT.toLocaleString()} (~ {Math.round(CHARACTER_LIMIT / 5)} words)
                </div>
              </div>

              <Textarea
                placeholder="Paste your AI-generated text here..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="min-h-[180px] resize-none"
                maxLength={CHARACTER_LIMIT}
              />

              <div className="flex gap-2">
                {isFreeLimit ? (
                  <Button className="flex-1" asChild>
                    <a href="/pricing">Continue Reframing</a>
                  </Button>
                ) : (
                  <Button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="flex-1"
                  >
                    {loading ? "Reframing..." : "Reframe"}
                  </Button>
                )}
              </div>

              {!hasActiveSubscription && (
                <p className="text-center text-sm font-medium text-primary">
                  Want to reframe entire books? <a href="/pricing" className="underline hover:no-underline">Go Pro!</a>
                </p>
              )}

              {output && (
                <>
                  <Textarea
                    value={output}
                    readOnly
                    className="min-h-[180px] bg-green-50 dark:bg-green-900/20"
                  />
                  <Button variant="secondary" onClick={copyOutput} className="w-full">
                    Copy Output
                  </Button>
                </>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

export default function Home() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading...</div>}>
      <HomeContent />
    </Suspense>
  );
}
