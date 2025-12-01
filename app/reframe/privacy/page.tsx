import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy Policy - Reframe",
  description: "Reframe Privacy Policy. Learn how we collect, use, and protect your data. We don't permanently store your text. GDPR and CCPA compliant. Last updated November 3, 2025.",
  keywords: ["privacy policy", "data protection", "GDPR", "CCPA", "data privacy", "reframe AI privacy"],
  openGraph: {
    title: "Privacy Policy - Reframe",
    description: "Learn how Reframe protects your privacy. We don't permanently store your text. GDPR and CCPA compliant.",
    type: "website",
    siteName: "Reframe",
  },
  twitter: {
    card: "summary",
    title: "Privacy Policy - Reframe",
    description: "Learn how Reframe protects your privacy and data.",
  },
  alternates: {
    canonical: "/privacy",
  },
};

export default function Privacy() {
  return (
    <div className="container mx-auto p-8 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">Privacy Policy</h1>
      <p className="text-sm text-muted-foreground mb-8">Last Updated: November 3, 2025</p>

      <div className="space-y-6">
        <section>
          <h2 className="text-2xl font-semibold mb-3">1. Introduction</h2>
          <p className="mb-3">
            Welcome to Reframe (&quot;we,&quot; &quot;our,&quot; or &quot;us&quot;). We respect your privacy and are committed to protecting your personal data. 
            This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our AI text reframing service.
          </p>
          <p>
            By using Reframe, you agree to the collection and use of information in accordance with this policy.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">2. Information We Collect</h2>
          
          <h3 className="text-xl font-semibold mb-2 mt-4">2.1 Account Information</h3>
          <p className="mb-3">
            When you create an account, we collect:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Email address</li>
            <li>Name (if provided through authentication provider)</li>
            <li>Authentication provider information (Google, GitHub, or email)</li>
          </ul>
          <p className="mb-3">
            This information is collected and stored by Reframe in Upstash Redis when you authenticate using Google or GitHub OAuth. 
            We do not store passwords - authentication is handled by your chosen provider (Google or GitHub).
          </p>

          <h3 className="text-xl font-semibold mb-2 mt-4">2.2 Payment Information</h3>
          <p className="mb-3">
            When you purchase a subscription:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Payment information is processed directly by <a href="https://razorpay.com" target="_blank" rel="noopener noreferrer" className="text-primary underline hover:no-underline">Razorpay</a></li>
            <li>We do NOT store your credit card information on our servers</li>
            <li>We receive only transaction confirmations and subscription status from Razorpay</li>
          </ul>

          <h3 className="text-xl font-semibold mb-2 mt-4">2.3 Usage Data</h3>
          <p className="mb-3">
            We collect minimal usage data to enforce service limits:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Number of requests made (usage counters)</li>
            <li>Timestamps of requests</li>
            <li>Subscription tier and status</li>
          </ul>
          <p className="mb-3">
            This data is stored in Upstash Redis and is temporary (see Data Retention below).
          </p>

          <h3 className="text-xl font-semibold mb-2 mt-4">2.4 Text Content</h3>
          <p className="mb-3">
            <strong>Important:</strong> Your input and output text is:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li><strong>Temporarily processed</strong> by our service and Groq&apos;s AI API</li>
            <li><strong>NOT stored permanently</strong> in any database</li>
            <li>Processed in memory only and discarded after the response is generated</li>
            <li>Sent to <a href="https://groq.com" target="_blank" rel="noopener noreferrer" className="text-primary underline hover:no-underline">Groq</a> for AI processing (subject to Groq&apos;s privacy policy)</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">3. How We Use Your Information</h2>
          <p className="mb-3">We use the collected information to:</p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Provide and maintain the Reframe service</li>
            <li>Process your payments and manage subscriptions</li>
            <li>Enforce usage limits based on your subscription tier</li>
            <li>Send service-related notifications (payment confirmations, usage alerts)</li>
            <li>Respond to your support requests</li>
            <li>Monitor and improve our service quality and performance</li>
            <li>Detect and prevent fraud or abuse</li>
          </ul>
          <p>
            We do NOT use your text content for training AI models or any other purpose beyond providing the immediate service response.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">4. Third-Party Service Providers</h2>
          <p className="mb-3">
            We use trusted third-party services to operate Reframe. Your data may be processed by:
          </p>

          <div className="space-y-3 ml-4">
            <div>
              <h3 className="font-semibold"><a href="https://google.com" target="_blank" rel="noopener noreferrer" className="text-primary underline hover:no-underline">Google OAuth</a></h3>
              <p className="text-sm">Optional authentication provider if you choose to sign in with Google. Google authenticates your identity and provides your email and name. We do not receive your Google password.</p>
            </div>

            <div>
              <h3 className="font-semibold"><a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-primary underline hover:no-underline">GitHub OAuth</a></h3>
              <p className="text-sm">Optional authentication provider if you choose to sign in with GitHub. GitHub authenticates your identity and provides your email and name. We do not receive your GitHub password.</p>
            </div>

            <div>
              <h3 className="font-semibold"><a href="https://razorpay.com" target="_blank" rel="noopener noreferrer" className="text-primary underline hover:no-underline">Razorpay</a></h3>
              <p className="text-sm">Payment processing. Handles all payment information securely. PCI-DSS Level 1 certified.</p>
            </div>

            <div>
              <h3 className="font-semibold"><a href="https://groq.com" target="_blank" rel="noopener noreferrer" className="text-primary underline hover:no-underline">Groq</a></h3>
              <p className="text-sm">AI text processing. Your input text is sent to Groq&apos;s API for reframing. Text is not permanently stored by Groq per their privacy policy.</p>
            </div>

            <div>
              <h3 className="font-semibold"><a href="https://upstash.com" target="_blank" rel="noopener noreferrer" className="text-primary underline hover:no-underline">Upstash</a></h3>
              <p className="text-sm">User account data storage, session management, usage tracking, and rate limiting. Stores your email, name, authentication provider, session data, usage counters, subscription status, and credit balance.</p>
            </div>
          </div>

          <p className="mt-3">
            Each service has its own privacy policy. We recommend reviewing their policies to understand how they handle your data.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">5. Data Retention</h2>
          <ul className="list-disc pl-6 mb-3 space-y-2">
            <li><strong>User text content:</strong> Not stored. Processed in memory only and immediately discarded after response generation.</li>
            <li><strong>Usage counters:</strong> Stored temporarily:
              <ul className="list-circle pl-6 mt-1 space-y-1">
                <li>Free tier: 24 hours (daily limit tracking)</li>
                <li>Pro tiers: No usage counting (unlimited)</li>
              </ul>
            </li>
            <li><strong>Account data:</strong> Retained until you delete your account</li>
            <li><strong>Payment records:</strong> Retained by Razorpay per legal requirements (typically 7 years for tax purposes)</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">6. Consent Tracking</h2>
          <p className="mb-3">
            We track your acceptance of our Terms of Service and Privacy Policy to comply with legal requirements:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li><strong>What we record:</strong> Timestamp of acceptance, document versions accepted, and optionally your IP address</li>
            <li><strong>Why we track:</strong> To demonstrate compliance with GDPR and CCPA consent requirements</li>
            <li><strong>Where it&apos;s stored:</strong> Upstash Redis database with key format: consent:&#123;userId&#125;</li>
            <li><strong>How to view:</strong> Your consent details are shown in your Account Settings page</li>
          </ul>
          <p>
            You must accept our Terms and Privacy Policy before creating an account. This consent is required to use the service.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">7. Your Rights (GDPR/CCPA)</h2>
          <p className="mb-3">Depending on your location, you have the following rights:</p>
          
          <ul className="list-disc pl-6 mb-3 space-y-2">
            <li><strong>Right to Access:</strong> Request a copy of your personal data we hold (self-service via Account Settings → Export Data)</li>
            <li><strong>Right to Deletion:</strong> Request deletion of your account and associated data (self-service via Account Settings → Delete Account)</li>
            <li><strong>Right to Correction:</strong> Request correction of inaccurate personal data</li>
            <li><strong>Right to Data Portability:</strong> Request your data in a portable format (JSON export available in Settings)</li>
            <li><strong>Right to Opt-Out:</strong> Opt out of marketing communications (we send minimal emails)</li>
            <li><strong>Right to Object:</strong> Object to certain data processing activities</li>
            <li><strong>Manage Subscription:</strong> Manage your subscription through Account Settings or the Pricing page</li>
          </ul>

          <p className="mb-3">
            <strong>Self-Service Options:</strong> You can exercise most rights directly through your Account Settings page without contacting support.
          </p>
          <p className="mb-3">
            For rights that require manual assistance, contact us at: <a href="mailto:writetokushaldsamant@gmail.com" className="text-primary underline">writetokushaldsamant@gmail.com</a>
          </p>
          <p>
            We will respond to your request within 30 days as required by law.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">8. International Data Transfers</h2>
          <p className="mb-3">
            Reframe operates globally, and your data may be processed in countries outside your own. Our third-party providers 
            (NextAuth.js, Razorpay, Groq, Upstash) may process data in the United States and other jurisdictions.
          </p>
          <p>
            When we transfer data internationally, we ensure appropriate safeguards are in place, such as:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Standard Contractual Clauses approved by the European Commission</li>
            <li>Privacy Shield frameworks (where applicable)</li>
            <li>Adequacy decisions</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">9. Cookies and Tracking</h2>
          <p className="mb-3">Reframe uses minimal cookies and browser storage:</p>
          <ul className="list-disc pl-6 mb-3 space-y-2">
            <li><strong>Essential Cookies:</strong> Authentication cookies from NextAuth.js to keep you logged in</li>
            <li><strong>Session Management:</strong> Temporary session data to maintain your login state</li>
            <li><strong>Cookie Consent:</strong> localStorage to remember your cookie consent preference</li>
            <li><strong>Consent Tracking:</strong> We display a cookie consent banner on your first visit</li>
          </ul>
          <p>
            We do NOT use:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Advertising or tracking cookies</li>
            <li>Third-party analytics services (like Google Analytics)</li>
            <li>Social media tracking pixels</li>
            <li>Non-essential cookies of any kind</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">10. Data Security</h2>
          <p className="mb-3">
            We take data security seriously and implement industry-standard measures:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>HTTPS encryption for all data in transit</li>
            <li>Trusted, security-certified third-party providers</li>
            <li>Regular security updates and monitoring</li>
            <li>Limited data retention (we don&apos;t store what we don&apos;t need)</li>
          </ul>
          <p>
            However, no method of transmission over the internet is 100% secure. While we strive to protect your data, 
            we cannot guarantee absolute security.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">11. Children&apos;s Privacy</h2>
          <p>
            Reframe is not intended for users under 13 years of age. We do not knowingly collect personal information 
            from children under 13. If you believe we have collected data from a child under 13, please contact us immediately, 
            and we will delete the information.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">12. Changes to This Privacy Policy</h2>
          <p className="mb-3">
            We may update this Privacy Policy from time to time to reflect changes in our practices or legal requirements. 
            We will notify you of any material changes by:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Posting the new Privacy Policy on this page</li>
            <li>Updating the &quot;Last Updated&quot; date at the top</li>
            <li>Sending an email notification for significant changes (if you have an account)</li>
          </ul>
          <p>
            Your continued use of Reframe after changes become effective constitutes acceptance of the updated policy.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">13. Contact Us</h2>
          <p className="mb-3">
            If you have questions, concerns, or requests regarding this Privacy Policy or your personal data, please contact us:
          </p>
          <ul className="list-none mb-3 space-y-1">
            <li><strong>Email:</strong> <a href="mailto:writetokushaldsamant@gmail.com" className="text-primary underline">writetokushaldsamant@gmail.com</a></li>
            <li><strong>Privacy Inquiries:</strong> <a href="mailto:writetokushaldsamant@gmail.com" className="text-primary underline">writetokushaldsamant@gmail.com</a></li>
          </ul>
          <p>
            We will respond to your inquiry within a reasonable timeframe, typically within 30 days.
          </p>
        </section>

        <div className="mt-8 p-4 bg-muted rounded-lg">
          <p className="text-sm text-muted-foreground">
            <strong>Summary:</strong> We collect minimal data (email, usage counters) to provide our service. Your text is NOT permanently stored. 
            We use trusted providers (NextAuth.js, Razorpay, Groq) who process data securely. You have full rights to access, delete, or export your data. 
            Contact us anytime with questions.
          </p>
        </div>
      </div>
    </div>
  );
}
