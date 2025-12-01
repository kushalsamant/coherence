'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface TourStep {
  id: string;
  title: string;
  description: string;
  target?: string; // CSS selector for element to highlight
}

const tourSteps: TourStep[] = [
  {
    id: 'upload',
    title: 'Upload Your Sketch',
    description: 'Drag and drop or click to upload your architectural sketch (PNG, JPG, or PDF). We will detect walls, rooms, doors, and windows.',
    target: '[data-tour="upload"]'
  },
  {
    id: 'process',
    title: 'Processing',
    description: 'Wait 30-60 seconds while we analyze your sketch and generate a professional BIM model. You\'ll see real-time progress updates.',
    target: '[data-tour="process"]'
  },
  {
    id: 'iterate',
    title: 'Edit & Iterate',
    description: 'Open the IFC viewer to explore your model. Use Edit Mode to make changes and create iterations. Generate layout variations to explore different arrangements.',
    target: '[data-tour="iterate"]'
  }
];

export default function QuickTour() {
  const [currentStep, setCurrentStep] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // Check if user has seen tour before
    const hasSeenTour = localStorage.getItem('sketch2bim_tour_completed');
    
    // Don't show immediately - wait for scroll
    if (hasSeenTour) {
      return;
    }

    // Set up scroll event listener
    const handleScroll = () => {
      setIsVisible(true);
      // Remove listener after first scroll
      window.removeEventListener('scroll', handleScroll);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });

    // Cleanup on unmount
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, []);

  const handleNext = () => {
    if (currentStep < tourSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleComplete();
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSkip = () => {
    handleComplete();
  };

  const handleComplete = () => {
    localStorage.setItem('sketch2bim_tour_completed', 'true');
    setIsVisible(false);
  };

  if (!isVisible) {
    return null;
  }

  const step = tourSteps[currentStep];
  const isFirst = currentStep === 0;
  const isLast = currentStep === tourSteps.length - 1;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      {/* Overlay with cutout for target element */}
      <div className="absolute inset-0" onClick={handleSkip}></div>
      
      {/* Tour Card */}
      <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full mx-4 z-10">
        {/* Progress Bar */}
        <div className="h-1 bg-gray-200">
          <div
            className="h-full bg-primary-600 transition-all duration-300"
            style={{ width: `${((currentStep + 1) / tourSteps.length) * 100}%` }}
          ></div>
        </div>

        {/* Content */}
        <div className="p-6">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-1">
                {step.title}
              </h3>
              <p className="text-sm text-gray-600">
                Step {currentStep + 1} of {tourSteps.length}
              </p>
            </div>
            <button
              onClick={handleSkip}
              className="text-gray-400 hover:text-gray-600"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <p className="text-gray-700 mb-6">{step.description}</p>

          {/* Navigation */}
          <div className="flex items-center justify-between">
            <button
              onClick={handlePrevious}
              disabled={isFirst}
              className="px-4 py-2 text-gray-700 rounded-lg hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Previous
            </button>

            <div className="flex gap-2">
              {tourSteps.map((_, index) => (
                <div
                  key={index}
                  className={`w-2 h-2 rounded-full ${
                    index === currentStep ? 'bg-primary-600' : 'bg-gray-300'
                  }`}
                ></div>
              ))}
            </div>

            <button
              onClick={handleNext}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              {isLast ? 'Get Started' : 'Next'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

