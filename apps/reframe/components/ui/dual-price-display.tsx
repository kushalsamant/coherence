"use client";

// Pricing configuration - unified across all apps (ASK, Reframe, Sketch2BIM)
const PRICING: Record<string, { amount: number; currency: string; symbol: string; interval?: string }> = {
  week: { amount: 1299, currency: "INR", symbol: "₹", interval: "week" },
  monthly: { amount: 3499, currency: "INR", symbol: "₹", interval: "month" },
  yearly: { amount: 29999, currency: "INR", symbol: "₹", interval: "year" },
};

function getDisplayPrice(priceKey: string) {
  return PRICING[priceKey] || { amount: 0, currency: "INR", symbol: "₹" };
}

function formatPrice(price: { amount: number; currency: string; symbol: string }) {
  return `${price.symbol}${price.amount.toLocaleString('en-IN')}`;
}
import { useState, useEffect } from "react";

interface DualPriceDisplayProps {
  priceKey: string;
  showInterval?: boolean;
  className?: string;
}

interface ExchangeRates {
  USD: number;
  EUR: number;
  GBP: number;
  source: string;
}

export function DualPriceDisplay({ 
  priceKey, 
  showInterval = true,
  className = "" 
}: DualPriceDisplayProps) {
  const price = getDisplayPrice(priceKey as any);
  const priceFormatted = formatPrice(price);
  const [rates, setRates] = useState<ExchangeRates | null>(null);
  
  // Fetch exchange rates on mount
  useEffect(() => {
    fetch("/api/exchange-rates")
      .then(res => res.json())
      .then(data => setRates(data))
      .catch(err => console.error("Failed to fetch exchange rates:", err));
  }, []);
  
  // Calculate conversions
  const usd = rates ? (price.amount * rates.USD).toFixed(2) : null;
  const eur = rates ? (price.amount * rates.EUR).toFixed(2) : null;
  const gbp = rates ? (price.amount * rates.GBP).toFixed(2) : null;
  
  return (
    <div className={`flex flex-col items-start ${className}`}>
      <div className="flex items-baseline gap-2 flex-wrap">
        <span className="text-4xl font-bold text-gray-900">
          {priceFormatted}
        </span>
      </div>
      {showInterval && price.interval && (
        <span className="text-sm text-gray-600 mt-1">
          per {price.interval}
        </span>
      )}
      {rates && (usd || eur || gbp) && (
        <span className="text-xs text-gray-500 mt-1">
          ≈ ${usd} USD, €{eur} EUR, £{gbp} GBP
        </span>
      )}
    </div>
  );
}

