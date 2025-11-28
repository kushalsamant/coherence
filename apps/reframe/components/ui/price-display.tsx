"use client";

import { useState, useRef, useEffect } from "react";

interface PriceDisplayProps {
  usd: number;
  className?: string;
  showCurrency?: boolean;
}

// Fallback exchange rates (used while loading or if API fails)
const FALLBACK_EUR_RATE = 0.92; // 1 USD = 0.92 EUR
const FALLBACK_INR_RATE = 83.0; // 1 USD = 83 INR

export function PriceDisplay({ usd, className = "", showCurrency = true }: PriceDisplayProps) {
  const [showTooltip, setShowTooltip] = useState(false);
  const [eurRate, setEurRate] = useState(FALLBACK_EUR_RATE);
  const [inrRate, setInrRate] = useState(FALLBACK_INR_RATE);
  const [ratesSource, setRatesSource] = useState<"loading" | "api" | "cache" | "fallback">("loading");
  const priceRef = useRef<HTMLSpanElement>(null);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  
  // Fetch live exchange rates on mount
  useEffect(() => {
    const fetchRates = async () => {
      try {
        const response = await fetch("/api/exchange-rates");
        const data = await response.json();
        
        if (data.EUR && data.INR) {
          setEurRate(data.EUR);
          setInrRate(data.INR);
          setRatesSource(data.source || "api");
        } else {
          setRatesSource("fallback");
        }
      } catch (error) {
        console.error("Failed to fetch exchange rates:", error);
        setRatesSource("fallback");
      }
    };
    
    fetchRates();
  }, []);
  
  const eur = (usd * eurRate).toFixed(2);
  const inr = Math.round(usd * inrRate);
  
  // Detect if device supports touch
  const isTouchDevice = typeof window !== "undefined" && ("ontouchstart" in window || navigator.maxTouchPoints > 0);
  
  // Auto-dismiss tooltip after 3 seconds on mobile
  useEffect(() => {
    if (showTooltip && isTouchDevice) {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      timeoutRef.current = setTimeout(() => {
        setShowTooltip(false);
      }, 3000);
    }
    
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [showTooltip, isTouchDevice]);
  
  // Handle keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (document.activeElement !== priceRef.current) return;
      
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        setShowTooltip((prev) => !prev);
      } else if (e.key === "Escape") {
        setShowTooltip(false);
      }
    };
    
    const handleClickOutside = (e: MouseEvent | TouchEvent) => {
      if (priceRef.current && !priceRef.current.contains(e.target as Node)) {
        setShowTooltip(false);
      }
    };
    
    document.addEventListener("keydown", handleKeyDown);
    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("touchstart", handleClickOutside);
    
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("touchstart", handleClickOutside);
    };
  }, []);
  
  // Mobile: tap to toggle, Desktop: hover
  const handleInteraction = () => {
    if (isTouchDevice) {
      setShowTooltip((prev) => !prev);
    } else {
      setShowTooltip(true);
    }
  };
  
  const handleLeave = () => {
    if (!isTouchDevice) {
      setShowTooltip(false);
    }
  };
  
  return (
    <span
      ref={priceRef}
      role="button"
      tabIndex={0}
      aria-expanded={showTooltip}
      aria-label={`Price: $${usd} USD. ${isTouchDevice ? "Tap" : "Hover"} to see conversions in EUR and INR.`}
      aria-describedby={showTooltip ? `price-tooltip-${usd}` : undefined}
      className={`relative inline-block ${isTouchDevice ? "cursor-pointer" : "cursor-help"} focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 rounded ${className}`}
      onMouseEnter={handleInteraction}
      onMouseLeave={handleLeave}
      onClick={handleInteraction}
      onTouchStart={(e) => {
        e.stopPropagation();
        handleInteraction();
      }}
    >
      ${usd}{showCurrency ? " USD" : ""}
      {isTouchDevice && (
        <span className="ml-1 text-xs opacity-60" aria-hidden="true">ⓘ</span>
      )}
      
      {showTooltip && (
        <span
          id={`price-tooltip-${usd}`}
          role="tooltip"
          className={`absolute ${isTouchDevice ? "bottom-full mb-2" : "bottom-full mb-2"} left-1/2 -translate-x-1/2 px-3 py-2 bg-slate-900 text-white text-sm rounded-lg whitespace-nowrap z-50 shadow-lg`}
        >
          <div className="space-y-1">
            <div>€{eur} EUR</div>
            <div>₹{inr} INR</div>
          </div>
          <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-1">
            <div className="border-4 border-transparent border-t-slate-900"></div>
          </div>
        </span>
      )}
    </span>
  );
}

