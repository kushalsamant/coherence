'use client';

import { useState, useEffect } from 'react';

interface RotatingTextProps {
  words: string[];
  interval?: number; // milliseconds
  className?: string;
}

export default function RotatingText({ 
  words, 
  interval = 2500,
  className = '' 
}: RotatingTextProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    if (words.length === 0) return;

    const timer = setInterval(() => {
      // Fade out
      setIsVisible(false);
      
      // After fade out, change word and fade in
      setTimeout(() => {
        setCurrentIndex((prevIndex) => (prevIndex + 1) % words.length);
        setIsVisible(true);
      }, 300); // Half of transition duration
    }, interval);

    return () => clearInterval(timer);
  }, [words, interval]);

  if (words.length === 0) {
    return null;
  }

  return (
    <span 
      className={`inline-block transition-opacity duration-300 ${className} ${
        isVisible ? 'opacity-100' : 'opacity-0'
      }`}
      aria-live="polite"
      aria-label={`Currently showing: ${words[currentIndex]}`}
    >
      {words[currentIndex]}
    </span>
  );
}

