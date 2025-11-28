import { Metadata } from "next";

export const metadata: Metadata = {
  title: "Terms of Service - Reframe",
  description: "Read Reframe's Terms of Service. Learn about our subscription plans, payment policies, acceptable use, and user rights. Last updated November 3, 2025.",
  keywords: ["terms of service", "user agreement", "reframe AI terms", "legal", "subscription terms"],
  openGraph: {
    title: "Terms of Service - Reframe",
    description: "Read Reframe's Terms of Service. Learn about our subscription plans, payment policies, and user rights.",
    type: "website",
    siteName: "Reframe",
  },
  twitter: {
    card: "summary",
    title: "Terms of Service - Reframe",
    description: "Read Reframe's Terms of Service and user agreement.",
  },
  alternates: {
    canonical: "/terms",
  },
};

export default function Terms() {
  return (
    <div className="container mx-auto p-8 max-w-4xl">
      <h1 className="text-3xl font-bold mb-6">Terms of Service</h1>
      <p className="text-sm text-muted-foreground mb-8">Last Updated: November 3, 2025</p>

      <div className="space-y-6">
        <section>
          <h2 className="text-2xl font-semibold mb-3">1. Acceptance of Terms</h2>
          <p className="mb-3">
            Welcome to Reframe. By accessing or using our service, you agree to be bound by these Terms of Service (&quot;Terms&quot;). 
            If you do not agree to these Terms, please do not use our service.
          </p>
          <p>
            These Terms constitute a legally binding agreement between you and Reframe. We reserve the right to update these 
            Terms at any time, and your continued use of the service constitutes acceptance of any changes.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">2. Service Description</h2>
          <p className="mb-3">
            Reframe is an AI-powered text reframing service that transforms AI-generated text into authentic human voices. 
            Our service:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Processes your text using artificial intelligence (Groq&apos;s Llama 3.1 model)</li>
            <li>Offers 6 distinct writing tones and voices</li>
            <li>Supports various character limits based on subscription tier</li>
            <li>Does NOT permanently store your input or output text</li>
          </ul>
          <p>
            <strong>What We Don&apos;t Do:</strong> We are not a content creation service, plagiarism tool, or professional writing service. 
            We do not guarantee the accuracy, quality, appropriateness, or originality of AI-generated output.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">3. User Accounts</h2>
          
          <h3 className="text-xl font-semibold mb-2 mt-4">3.1 Account Creation</h3>
          <p className="mb-3">
            To use Reframe, you must create an account by signing in with:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Google account (via Google OAuth)</li>
            <li>GitHub account (via GitHub OAuth)</li>
          </ul>
          <p className="mb-3">
            Authentication is handled securely by Google or GitHub. We do not store passwords. Your session and account data are stored in Upstash Redis.
          </p>

          <h3 className="text-xl font-semibold mb-2 mt-4">3.2 Account Security</h3>
          <p className="mb-3">You are responsible for:</p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Maintaining the confidentiality of your account credentials</li>
            <li>All activities that occur under your account</li>
            <li>Notifying us immediately of any unauthorized use</li>
          </ul>

          <h3 className="text-xl font-semibold mb-2 mt-4">3.3 Age Requirement</h3>
          <p>
            You must be at least 13 years old to use Reframe. By using our service, you represent that you meet this age requirement.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">4. Subscription Plans and Payments</h2>
          
          <h3 className="text-xl font-semibold mb-2 mt-4">4.1 Service Tiers</h3>
          
          <div className="ml-4 space-y-3">
            <div>
              <h4 className="font-semibold">Free Tier (₹0)</h4>
              <ul className="list-disc pl-6 text-sm space-y-1">
                <li>5 requests total (one-time)</li>
                <li>3 essential tones: Conversational, Professional, Academic</li>
                <li>Age targeting included</li>
                <li>10,000 words (~50,000 characters) per request</li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold">Daily Pass (₹99 INR one-time)</h4>
              <ul className="list-disc pl-6 text-sm space-y-1">
                <li>Unlimited requests for 24 hours</li>
                <li>All 6 tones unlocked</li>
                <li>Age targeting included</li>
                <li>10,000 words per request</li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold">Monthly Pro (₹999 INR/month)</h4>
              <ul className="list-disc pl-6 text-sm space-y-1">
                <li>Unlimited requests</li>
                <li>All 6 tones unlocked</li>
                <li>Age targeting included</li>
                <li>10,000 words per request</li>
                <li>Priority support</li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold">Yearly Pro (₹7,999 INR/year)</h4>
              <ul className="list-disc pl-6 text-sm space-y-1">
                <li>Unlimited requests</li>
                <li>All 6 tones unlocked</li>
                <li>Age targeting included</li>
                <li>10,000 words per request</li>
                <li>Priority support</li>
                <li>Early access to new features</li>
                <li>33% savings compared to monthly</li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold">Credit Packs (One-Time Purchase)</h4>
              <ul className="list-disc pl-6 text-sm space-y-1">
                <li>10-Credit Pack: ₹299 INR (₹29.90 per request)</li>
                <li>30-Credit Pack: ₹699 INR (₹23.30 per request)</li>
                <li>100-Credit Pack: ₹1,799 INR (₹17.99 per request)</li>
                <li>Credits never expire</li>
                <li>All 6 tones and age targeting unlocked</li>
              </ul>
            </div>
          </div>

          <h3 className="text-xl font-semibold mb-2 mt-4">4.2 Payment Processing</h3>
          <p className="mb-3">
            All payments are processed securely through Razorpay. By subscribing or purchasing credits, you agree to:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Provide accurate payment information</li>
            <li>Authorize us to charge your payment method</li>
            <li>Be bound by Razorpay&apos;s Terms of Service</li>
          </ul>

          <h3 className="text-xl font-semibold mb-2 mt-4">4.3 Billing and Auto-Renewal</h3>
          <ul className="list-disc pl-6 mb-3 space-y-2">
            <li>Subscriptions automatically renew at the end of each billing period (weekly, monthly, or yearly)</li>
            <li>You will be charged at the beginning of each renewal period</li>
            <li>You can cancel auto-renewal at any time through your account settings or the Pricing page</li>
            <li>Cancellation takes effect at the end of the current billing period</li>
          </ul>

          <h3 className="text-xl font-semibold mb-2 mt-4">4.4 Refund Policy</h3>
          <ul className="list-disc pl-6 mb-3 space-y-2">
            <li><strong>Subscriptions:</strong> If you cancel within 7 days of initial purchase and have used fewer than 5 requests, 
            you may request a full refund. After 7 days, subscription fees are non-refundable, but you can cancel to prevent future charges.</li>
            <li><strong>Credit Packs:</strong> Credit packs are non-refundable once purchased, as credits never expire and provide 
            permanent access to premium features.</li>
            <li><strong>Pro-rated refunds:</strong> We do not offer pro-rated refunds for partial billing periods.</li>
          </ul>
          <p className="mb-3">
            To request a refund, contact us at <a href="mailto:writetokushaldsamant@gmail.com" className="text-primary underline">writetokushaldsamant@gmail.com</a> 
            within the eligible timeframe.
          </p>

          <h3 className="text-xl font-semibold mb-2 mt-4">4.5 Price Changes</h3>
          <p>
            We reserve the right to change our pricing at any time. Price changes will not affect existing subscriptions until renewal. 
            We will notify you of price changes at least 30 days before they take effect.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">5. Acceptable Use Policy</h2>
          <p className="mb-3">You agree NOT to use Reframe for:</p>
          
          <h3 className="text-xl font-semibold mb-2 mt-4">5.1 Prohibited Content</h3>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Illegal activities or content that violates any applicable laws</li>
            <li>Harassment, threats, hate speech, or violent content</li>
            <li>Content that infringes on intellectual property rights</li>
            <li>Spam, phishing, or deceptive content</li>
            <li>Malware, viruses, or malicious code</li>
            <li>Child exploitation or endangerment in any form</li>
            <li>Sexually explicit content involving minors</li>
          </ul>

          <h3 className="text-xl font-semibold mb-2 mt-4">5.2 Prohibited Activities</h3>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Automated access, scraping, or bot usage without written permission</li>
            <li>Attempting to circumvent usage limits or payment requirements</li>
            <li>Reverse engineering, decompiling, or attempting to extract our source code</li>
            <li>Reselling or redistributing our service without authorization</li>
            <li>Impersonating others or providing false information</li>
            <li>Interfering with or disrupting the service or servers</li>
          </ul>

          <p className="mt-3">
            Violation of this Acceptable Use Policy may result in immediate account suspension or termination without refund.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">6. Intellectual Property Rights</h2>
          
          <h3 className="text-xl font-semibold mb-2 mt-4">6.1 Your Content</h3>
          <p className="mb-3">You retain all ownership rights to:</p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Text you input into Reframe</li>
            <li>Text output generated by the service</li>
          </ul>
          <p className="mb-3">
            By using our service, you grant us a temporary, non-exclusive license to process your input text solely for the 
            purpose of providing the service. We do not claim ownership of your content.
          </p>

          <h3 className="text-xl font-semibold mb-2 mt-4">6.2 Our Intellectual Property</h3>
          <p className="mb-3">Reframe owns all rights to:</p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>The Reframe website, application, and service</li>
            <li>Our brand, logo, and trademarks</li>
            <li>Our proprietary algorithms, prompts, and processes</li>
            <li>All software, code, and technical infrastructure</li>
          </ul>

          <h3 className="text-xl font-semibold mb-2 mt-4">6.3 No Copyright Guarantee</h3>
          <p>
            <strong>Important:</strong> We do not guarantee that AI-generated output is original, copyright-free, or does not 
            infringe on third-party rights. You are responsible for reviewing and verifying the output before use. We are not 
            liable for any copyright infringement claims arising from your use of the output.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">7. Third-Party Services</h2>
          <p className="mb-3">
            Reframe relies on third-party services to operate. By using our service, you acknowledge that your data will be 
            processed by:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-2">
            <li><strong><a href="https://google.com" target="_blank" rel="noopener noreferrer" className="text-primary underline hover:no-underline">Google OAuth</a>:</strong> Optional authentication provider if you sign in with Google</li>
            <li><strong><a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-primary underline hover:no-underline">GitHub OAuth</a>:</strong> Optional authentication provider if you sign in with GitHub</li>
            <li><strong><a href="https://razorpay.com" target="_blank" rel="noopener noreferrer" className="text-primary underline hover:no-underline">Razorpay</a>:</strong> Payment processing</li>
            <li><strong><a href="https://groq.com" target="_blank" rel="noopener noreferrer" className="text-primary underline hover:no-underline">Groq</a>:</strong> AI text processing - your input text is sent to Groq&apos;s API</li>
            <li><strong><a href="https://upstash.com" target="_blank" rel="noopener noreferrer" className="text-primary underline hover:no-underline">Upstash</a>:</strong> User account data, session management, usage tracking, and rate limiting</li>
          </ul>
          <p className="mb-3">
            Each third-party service has its own terms of service and privacy policy. We are not responsible for the practices 
            or policies of these third parties.
          </p>
          <p>
            <strong>Note:</strong> Groq processes your text to generate the reframed output. While Groq does not permanently 
            store your text per their policy, transmission to a third-party AI service is inherent to how our service works.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">8. AI Service Disclaimers</h2>
          <p className="mb-3">
            <strong>Reframe is an AI-powered service. You acknowledge and agree that:</strong>
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-2">
            <li>AI output may be inaccurate, inappropriate, biased, or contain errors</li>
            <li>We do not guarantee the quality, accuracy, or suitability of any output for your purposes</li>
            <li>Output may inadvertently include offensive, harmful, or inappropriate content</li>
            <li>You are solely responsible for reviewing, editing, and verifying all output before use</li>
            <li>Our service is NOT suitable for:
              <ul className="list-circle pl-6 mt-2 space-y-1">
                <li>Medical, legal, or professional advice</li>
                <li>Life-critical or safety-critical applications</li>
                <li>Academic submissions without disclosure and permission</li>
                <li>Any purpose where accuracy is essential without human review</li>
              </ul>
            </li>
          </ul>
          <p>
            <strong>You use AI-generated content at your own risk.</strong> We are not liable for any consequences of using 
            the output, including but not limited to academic penalties, professional consequences, or harm to third parties.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">9. Limitation of Liability</h2>
          
          <h3 className="text-xl font-semibold mb-2 mt-4">9.1 &quot;As Is&quot; Service</h3>
          <p className="mb-3">
            REFRAME AI IS PROVIDED &quot;AS IS&quot; AND &quot;AS AVAILABLE&quot; WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, 
            INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.
          </p>

          <h3 className="text-xl font-semibold mb-2 mt-4">9.2 No Liability for Damages</h3>
          <p className="mb-3">
            TO THE MAXIMUM EXTENT PERMITTED BY LAW, REFRAME AI AND ITS AFFILIATES SHALL NOT BE LIABLE FOR:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Indirect, incidental, special, consequential, or punitive damages</li>
            <li>Loss of profits, revenue, data, or business opportunities</li>
            <li>Service interruptions, errors, or downtime</li>
            <li>Any damages arising from your use of AI-generated content</li>
            <li>Actions or inactions of third-party service providers</li>
          </ul>

          <h3 className="text-xl font-semibold mb-2 mt-4">9.3 Maximum Liability</h3>
          <p>
            Our total liability to you for any claims arising from your use of Reframe shall not exceed the amount you paid 
            us in the 12 months prior to the event giving rise to the claim, or $100, whichever is less.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">10. Indemnification</h2>
          <p>
            You agree to indemnify, defend, and hold harmless Reframe, its officers, directors, employees, and affiliates from 
            any claims, damages, losses, liabilities, and expenses (including legal fees) arising from:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Your use or misuse of the service</li>
            <li>Your violation of these Terms</li>
            <li>Your violation of any laws or third-party rights</li>
            <li>Content you input or output you use</li>
            <li>Your breach of the Acceptable Use Policy</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">11. Data and Privacy</h2>
          <p className="mb-3">
            Your use of Reframe is also governed by our <a href="/privacy" className="text-primary underline">Privacy Policy</a>, 
            which explains how we collect, use, and protect your information.
          </p>
          <p>
            Key privacy points:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Your input and output text is NOT permanently stored</li>
            <li>We collect minimal data (email, usage counters)</li>
            <li>Third-party processors handle authentication, payments, and AI processing</li>
            <li>You have rights to access, delete, and export your data</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">12. Termination</h2>
          
          <h3 className="text-xl font-semibold mb-2 mt-4">12.1 By You</h3>
          <p className="mb-3">
            You may cancel your subscription or delete your account at any time. Cancellation takes effect at the end of your 
            current billing period, and you will retain access until then.
          </p>

          <h3 className="text-xl font-semibold mb-2 mt-4">12.2 By Us</h3>
          <p className="mb-3">We reserve the right to suspend or terminate your account immediately, without notice, if:</p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>You violate these Terms or our Acceptable Use Policy</li>
            <li>Your payment fails or your account is past due</li>
            <li>We suspect fraudulent, abusive, or illegal activity</li>
            <li>We decide to discontinue the service</li>
          </ul>
          <p>
            Termination for violation does not entitle you to a refund.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">13. Changes to Terms</h2>
          <p className="mb-3">
            We may update these Terms from time to time. We will notify you of material changes by:
          </p>
          <ul className="list-disc pl-6 mb-3 space-y-1">
            <li>Posting the updated Terms on this page with a new &quot;Last Updated&quot; date</li>
            <li>Sending an email notification to your registered email address</li>
          </ul>
          <p>
            Your continued use of Reframe after changes take effect constitutes acceptance of the new Terms. If you do not 
            agree with the changes, you must stop using the service and cancel your account.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">14. Governing Law and Dispute Resolution</h2>
          
          <h3 className="text-xl font-semibold mb-2 mt-4">14.1 Governing Law</h3>
          <p className="mb-3">
            These Terms are governed by the laws of India and the state of Maharashtra, without regard to conflict 
            of law principles.
          </p>

          <h3 className="text-xl font-semibold mb-2 mt-4">14.2 Dispute Resolution</h3>
          <p className="mb-3">
            Before filing a lawsuit, you agree to first contact us at <a href="mailto:writetokushaldsamant@gmail.com" className="text-primary underline">writetokushaldsamant@gmail.com</a> to 
            attempt to resolve the dispute informally.
          </p>
          <p>
            If we cannot resolve the dispute within 30 days, either party may pursue legal action in the appropriate courts 
            of Maharashtra, India.
          </p>

          <h3 className="text-xl font-semibold mb-2 mt-4">14.3 No Class Actions</h3>
          <p>
            You agree to resolve disputes individually and waive any right to participate in class action lawsuits or class-wide 
            arbitration.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">15. Miscellaneous</h2>
          <ul className="list-disc pl-6 mb-3 space-y-2">
            <li><strong>Entire Agreement:</strong> These Terms, along with our Privacy Policy, constitute the entire agreement 
            between you and Reframe.</li>
            <li><strong>Severability:</strong> If any provision is found unenforceable, the remaining provisions remain in effect.</li>
            <li><strong>No Waiver:</strong> Our failure to enforce any right or provision does not constitute a waiver of that right.</li>
            <li><strong>Assignment:</strong> You may not assign these Terms without our consent. We may assign our rights to any affiliate or successor.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-semibold mb-3">16. Contact Information</h2>
          <p className="mb-3">
            For questions, concerns, or notices regarding these Terms, please contact us:
          </p>
          <ul className="list-none mb-3 space-y-1">
            <li><strong>Email:</strong> <a href="mailto:writetokushaldsamant@gmail.com" className="text-primary underline">writetokushaldsamant@gmail.com</a></li>
            <li><strong>Legal Inquiries:</strong> <a href="mailto:writetokushaldsamant@gmail.com" className="text-primary underline">writetokushaldsamant@gmail.com</a></li>
          </ul>
        </section>

        <div className="mt-8 p-4 bg-muted rounded-lg">
          <p className="text-sm text-muted-foreground">
            <strong>Quick Summary:</strong> By using Reframe, you agree to use it responsibly and legally. We provide an AI text 
            service &quot;as is&quot; without guarantees. You own your content. Subscriptions auto-renew but can be cancelled anytime. We don&apos;t 
            store your text permanently. Violating our policies may result in account termination. For full details, please read the 
            complete Terms above.
          </p>
        </div>

        <div className="mt-4 p-4 bg-amber-50 border border-amber-200 rounded-lg">
          <p className="text-sm text-amber-900">
            <strong>⚠️ Legal Notice:</strong> These Terms are provided as a template. Before launching with real customers, please 
            have an attorney review and customize them for your specific business needs and jurisdiction.
          </p>
        </div>
      </div>
    </div>
  );
}
