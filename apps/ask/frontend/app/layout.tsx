import type { Metadata } from "next";
import { ThemeProvider, AppFooter } from "@kushalsamant/design-template";
import "@kushalsamant/design-template/styles/globals.css";
import { SessionProvider } from "next-auth/react";
import Link from "next/link";
import HeaderWrapper from "@/components/HeaderWrapper";

const socialLinks = [
  { href: 'https://github.com/kushalsamant', label: 'GitHub' },
  { href: 'https://linkedin.com/in/kvshvl', label: 'LinkedIn' },
  { href: 'https://kvshvl.medium.com', label: 'Medium' },
  { href: 'https://instagram.com/kvshvl', label: 'Instagram' },
  { href: 'https://twitter.com/kvshvl_', label: 'Twitter' },
  { href: 'https://youtube.com/@kvshvl', label: 'YouTube' },
];

export const metadata: Metadata = {
  title: "ASK: Daily Research - Research Q&A Tool",
  description: "Browse and generate research question-answer pairs with photorealistic images. Explore research themes including sustainability science, engineering systems, and more.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const currentYear = new Date().getFullYear();
  
  return (
    <html lang="en">
      <body>
        <ThemeProvider>
          <SessionProvider>
            {/* Skip to main content link for accessibility */}
            <a
              href="#main-content"
              className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-primary focus:text-primary-foreground focus:rounded-md focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              Skip to main content
            </a>
            <HeaderWrapper />
            <main id="main-content" role="main">
            {children}
          </main>
          <AppFooter
            legalLinks={[
              { href: 'https://kvshvl.in/privacypolicy', label: 'Privacy Policy' },
              { href: 'https://kvshvl.in/termsofservice', label: 'Terms of Service' },
              { href: 'https://kvshvl.in/cancellationrefund', label: 'Cancellation & Refund' },
              { href: 'https://kvshvl.in/getintouch', label: 'Get in Touch' },
            ]}
            socialLinks={socialLinks}
            branding={`© ${currentYear} Architect Kushal Dhananjay Samant. Licensed under the Architect's Act, 1972 of India.`}
            companyLink="https://kvshvl.in"
            companyLabel="KVSHVL"
            LinkComponent={Link}
          />
          </SessionProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
