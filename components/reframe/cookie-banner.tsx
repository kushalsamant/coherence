"use client";

import { useState, useEffect } from "react";
import { Button } from "./ui/button";

export function CookieBanner() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Check if user has already accepted cookies
    const cookieConsent = localStorage.getItem("cookieConsent");
    if (cookieConsent !== "accepted") {
      setIsVisible(true);
    }
  }, []);

  const acceptCookies = () => {
    localStorage.setItem("cookieConsent", "accepted");
    setIsVisible(false);
  };

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-slate-900 text-white p-4 shadow-lg z-50 border-t border-slate-700">
      <div className="container mx-auto max-w-6xl flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="text-sm text-slate-200">
          This website uses essential cookies for authentication only. Learn more in our{" "}
          <a
            href="/privacy"
            className="underline hover:text-white font-medium"
            target="_blank"
            rel="noopener noreferrer"
          >
            Privacy Policy
          </a>
          .
        </div>
        <Button
          onClick={acceptCookies}
          variant="secondary"
          size="sm"
          className="whitespace-nowrap"
        >
          Accept
        </Button>
      </div>
    </div>
  );
}

