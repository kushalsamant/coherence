import Link from 'next/link';
import { auth } from '@/app/sketch2bim/auth';
import QuickTour from '@/components/sketch2bim/QuickTour';
import RotatingText from '@/components/sketch2bim/RotatingText';

export default async function Home() {
  const session = await auth();

  return (
    <main className="min-h-screen">
      <QuickTour />
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h2 className="text-5xl font-bold text-gray-900 dark:text-gray-100 mb-6">
            Transform Sketches into{' '}
            <span className="text-primary-600">
              <RotatingText words={['BIM Models', 'IFC Files', 'DWG Drawings', 'Revit-Compatible', 'SketchUp Models', 'CAD Drawings']} />
            </span>
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
            Upload hand-drawn architectural sketches and get editable DWG, IFC (Revit-compatible), and SketchUp files in minutes.
          </p>
          <div className="flex gap-4 justify-center">
            {session ? (
              <Link href="/dashboard" className="btn-primary text-lg">
                Go to Dashboard
              </Link>
            ) : (
              <Link href="/api/auth/signin" className="btn-primary text-lg">
                Get Started Free
              </Link>
            )}
          </div>
        </div>

        {/* Features */}
        <div id="features" className="mt-24 grid md:grid-cols-3 gap-8">
          <div className="card text-center">
            <div className="text-4xl mb-4">🧠</div>
            <h3 className="text-xl font-semibold mb-2">Intelligent Processing</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Automatic quality gates ensure high-quality results. Multi-stage validation with adaptive parameter selection.
            </p>
          </div>
          
          <div className="card text-center">
            <div className="text-4xl mb-4">🏗️</div>
            <h3 className="text-xl font-semibold mb-2">Architectural Plans</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Optimized for architectural floor plans with automatic detection of walls, doors, windows, and room layouts.
            </p>
          </div>
          
          <div className="card text-center">
            <div className="text-4xl mb-4">📏</div>
            <h3 className="text-xl font-semibold mb-2">Auto-Legend Detection</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Automatically detects scale and labels from your sketches. No manual input needed - we read your legend.
            </p>
          </div>
          
          <div className="card text-center">
            <div className="text-4xl mb-4">✅</div>
            <h3 className="text-xl font-semibold mb-2">Standards Compliance</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Built-in quality control with auto-fixes. IDS validation ensures BIM standards compliance. QC reports included.
            </p>
          </div>
        </div>

        {/* Why Choose Us */}
        <div className="mt-24 bg-gray-50 dark:bg-gray-900 rounded-2xl p-12">
          <h2 className="text-3xl font-bold text-center mb-12 text-gray-900 dark:text-gray-100">Why Choose Sketch-to-BIM?</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-3xl mb-3">⚡</div>
              <h3 className="font-semibold mb-2 text-gray-900 dark:text-gray-100">Fast & Reliable</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">Lightweight processing with no desktop software required. Get results in minutes.</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-3">🌐</div>
              <h3 className="font-semibold mb-2 text-gray-900 dark:text-gray-100">Web-Based</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">No desktop software needed. Access from any device, anywhere.</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-3">🏢</div>
              <h3 className="font-semibold mb-2 text-gray-900 dark:text-gray-100">Enterprise Quality</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">Enterprise-grade quality control with confidence scoring and validation.</p>
            </div>
            <div className="text-center">
              <div className="text-3xl mb-3">📤</div>
              <h3 className="font-semibold mb-2 text-gray-900 dark:text-gray-100">Multi-Format Export</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">IFC (Revit-compatible), DWG, and SketchUp from one upload. All formats included.</p>
            </div>
          </div>
          
          <div className="mt-12 grid md:grid-cols-3 gap-6">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg">
              <h3 className="font-semibold mb-2 text-gray-900 dark:text-gray-100">Version Control</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">Iterations system tracks changes and versions of your BIM files.</p>
            </div>
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg">
              <h3 className="font-semibold mb-2 text-gray-900 dark:text-gray-100">Layout Variations</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">Generate alternative room arrangements from the same sketch.</p>
            </div>
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg">
              <h3 className="font-semibold mb-2 text-gray-900 dark:text-gray-100">Quality Reports</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">Detailed QC reports with confidence scores and validation results.</p>
            </div>
          </div>
        </div>

        {/* Pricing */}
        <div className="mt-24">
          <h2 className="text-3xl font-bold text-center mb-6 text-gray-900 dark:text-gray-100">Flexible, Time-Based Access</h2>
          <p className="text-center text-gray-600 dark:text-gray-400 mb-12">Every plan includes all features. Pick the time window that matches your deadline.</p>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { title: 'Trial', price: 'Free', caption: 'Unlimited conversions · 7 days', highlight: 'No card required', href: '/api/auth/signin', variant: 'secondary' },
              { title: 'Week Access', price: '₹1,299', caption: '7 days unlimited', highlight: 'Sprint-ready', href: '/pricing', variant: 'primary' },
              { title: 'Monthly Access', price: '₹3,499', caption: '30 days', highlight: 'Best for ongoing projects', href: '/pricing', variant: 'primary', featured: true },
              { title: 'Yearly Access', price: '₹29,999', caption: '365 days', highlight: 'Best value for power users', href: '/pricing', variant: 'primary' }
            ].map((plan) => (
              <div key={plan.title} className={`card relative ${plan.featured ? 'ring-2 ring-primary-600 shadow-lg' : ''}`}>
                {plan.featured && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary-600 text-white px-4 py-1 rounded-full text-xs font-semibold">
                    Most Popular
                  </div>
                )}
                <h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">{plan.title}</h3>
                <p className="text-3xl font-bold text-gray-900 dark:text-gray-100">{plan.price}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{plan.caption}</p>
                <p className="text-sm text-primary-600 dark:text-primary-400 font-medium mt-3">{plan.highlight}</p>
                <Link
                  href={plan.href}
                  className={`mt-6 inline-block w-full text-center px-4 py-2 rounded-lg ${
                    plan.variant === 'secondary'
                      ? 'border border-primary-600 text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/20'
                      : 'bg-primary-600 text-white hover:bg-primary-700'
                  }`}
                >
                  Choose {plan.title}
                </Link>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}

