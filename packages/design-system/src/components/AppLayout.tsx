/**
 * Standard Application Layout Component (Body Content Only)
 * Provides consistent layout structure inside the body tag
 * Layout files should wrap this with html/body tags and export metadata
 */
import React, { type ReactNode, type ComponentType } from "react";
import ThemeProvider from "./ThemeProvider";
import AppFooter from "./AppFooter";
// Note: SessionProvider removed - apps should use their own AuthProvider
// This component no longer wraps with SessionProvider to allow apps to use Supabase Auth
import type { AppLayoutProps } from "./AppLayoutProps";

const DEFAULT_SOCIAL_LINKS = [
  { href: 'https://github.com/kushalsamant', label: 'GitHub' },
  { href: 'https://linkedin.com/in/kvshvl', label: 'LinkedIn' },
  { href: 'https://kvshvl.medium.com', label: 'Medium' },
  { href: 'https://instagram.com/kvshvl', label: 'Instagram' },
  { href: 'https://twitter.com/kvshvl_', label: 'Twitter' },
  { href: 'https://youtube.com/@kvshvl', label: 'YouTube' },
];

const DEFAULT_LEGAL_LINKS = [
  { href: 'https://kvshvl.in/privacypolicy', label: 'Privacy Policy' },
  { href: 'https://kvshvl.in/termsofservice', label: 'Terms of Service' },
  { href: 'https://kvshvl.in/cancellationrefund', label: 'Cancellation & Refund' },
  { href: 'https://kvshvl.in/getintouch', label: 'Get in Touch' },
];

const DEFAULT_BRANDING = (year: number) => 
  `© ${year} Architect Kushal Dhananjay Samant. Licensed under the Architect's Act, 1972 of India.`;

export function AppLayout({
  header,
  legalLinks = DEFAULT_LEGAL_LINKS,
  socialLinks = DEFAULT_SOCIAL_LINKS,
  branding,
  companyLink = "https://kvshvl.in",
  companyLabel = "KVSHVL",
  footerBranding,
  additionalBodyContent = [],
  LinkComponent,
  children,
}: Omit<AppLayoutProps, 'metadata' | 'appName' | 'appDescription' | 'fontClassName' | 'lang' | 'additionalProviders'>) {
  const currentYear = new Date().getFullYear();
  const brandingText = branding || DEFAULT_BRANDING(currentYear);
  
  // Render header - can be a component or ReactNode
  let headerContent: ReactNode = null;
  if (header) {
    if (typeof header === 'function') {
      const HeaderComponent = header as ComponentType;
      headerContent = <HeaderComponent />;
    } else {
      headerContent = header;
    }
  }

  return (
    <ThemeProvider>
      {headerContent}
      <main role="main">
        {children}
      </main>
      <AppFooter
        legalLinks={legalLinks}
        socialLinks={socialLinks}
        branding={footerBranding || brandingText}
        companyLink={companyLink}
        companyLabel={companyLabel}
        LinkComponent={LinkComponent}
      />
      {additionalBodyContent.map((content, index) => (
        <React.Fragment key={index}>{content}</React.Fragment>
      ))}
    </ThemeProvider>
  );
}
