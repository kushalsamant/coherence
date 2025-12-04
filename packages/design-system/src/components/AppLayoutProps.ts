/**
 * AppLayout component props
 */
import type { ReactNode, ComponentType } from "react";
import type { Metadata } from "next";

export interface LegalLink {
  href: string;
  label: string;
}

export interface SocialLink {
  href: string;
  label: string;
}

export interface AppLayoutProps {
  /** Page metadata (title, description) */
  metadata?: Metadata;
  
  /** Application name for branding */
  appName: string;
  
  /** Application description for metadata */
  appDescription?: string;
  
  /** Header component to render */
  header?: ComponentType | ReactNode;
  
  /** Footer legal links */
  legalLinks?: LegalLink[];
  
  /** Footer social links */
  socialLinks?: SocialLink[];
  
  /** Footer branding text */
  branding?: string;
  
  /** Company link URL */
  companyLink?: string;
  
  /** Company label */
  companyLabel?: string;
  
  /** Custom footer branding component */
  footerBranding?: ReactNode;
  
  /** Show skip link for accessibility */
  showSkipLink?: boolean;
  
  /** Additional providers to wrap content with */
  additionalProviders?: ReactNode[];
  
  /** Additional content to render in body (e.g., Toaster, CookieBanner) */
  additionalBodyContent?: ReactNode[];
  
  /** Custom font configuration (e.g., Inter from next/font/google) */
  fontClassName?: string;
  
  /** HTML lang attribute */
  lang?: string;
  
  /** Link component for navigation (Next.js Link) */
  LinkComponent?: ComponentType<any>;
  
  /** Page content */
  children: ReactNode;
}

