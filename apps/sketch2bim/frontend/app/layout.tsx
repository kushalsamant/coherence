import type { Metadata } from 'next';
export const dynamic = 'force-dynamic';
import { Inter } from 'next/font/google';
import { ThemeProvider, AppFooter } from '@kushalsamant/design-template';
import '@kushalsamant/design-template/styles/globals.css';
import './globals.css';
import { SessionProvider } from 'next-auth/react';
import Link from 'next/link';
import HeaderWrapper from '@/components/HeaderWrapper';

const inter = Inter({ subsets: ['latin'] });

const socialLinks = [
  { href: 'https://github.com/kushalsamant', label: 'GitHub' },
  { href: 'https://linkedin.com/in/kvshvl', label: 'LinkedIn' },
  { href: 'https://kvshvl.medium.com', label: 'Medium' },
  { href: 'https://instagram.com/kvshvl', label: 'Instagram' },
  { href: 'https://twitter.com/kvshvl_', label: 'Twitter' },
  { href: 'https://youtube.com/@kvshvl', label: 'YouTube' },
];

export const metadata: Metadata = {
  title: 'Sketch-to-BIM',
  description: 'Convert architectural sketches to editable BIM models using computer vision',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const currentYear = new Date().getFullYear();
  
  return (
    <html lang="en" className={inter.className}>
      <body>
        <ThemeProvider>
          <SessionProvider>
            <HeaderWrapper />
            {children}
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

