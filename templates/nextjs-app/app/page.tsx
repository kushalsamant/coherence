import Link from "next/link";

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-16">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Welcome to {{APP_DISPLAY_NAME}}</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">
          {{APP_DESCRIPTION}}
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/pricing"
            className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            View Pricing
          </Link>
          <Link
            href="/settings"
            className="px-6 py-3 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
          >
            Settings
          </Link>
        </div>
      </div>
    </div>
  );
}

