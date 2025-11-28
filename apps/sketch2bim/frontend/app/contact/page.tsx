'use client';

import Link from 'next/link';
import { LegalPageLayout, ContactPage, AppFooter } from '@kushalsamant/design-template';

export default function ContactPageWrapper() {
  return (
    <LegalPageLayout
      title="Contact Us"
      appName="Sketch-to-BIM"
      homeLink="/"
      LinkComponent={Link}
      FooterComponent={() => (
        <AppFooter
          legalLinks={[
            { href: '/terms', label: 'Terms and Conditions' },
            { href: '/privacy', label: 'Privacy Policy' },
            { href: '/refund', label: 'Cancellation and Refund' },
            { href: '/shipping', label: 'Shipping and Exchange' },
            { href: '/contact', label: 'Contact Us' },
          ]}
          companyLink="https://kvshvl.in"
          companyLabel="KVSHVL"
          branding={`© {year} Sketch-to-BIM. All rights reserved.`}
          LinkComponent={Link}
          className="mt-24"
        />
      )}
    >
      <ContactPage
        appName="Sketch-to-BIM"
        LinkComponent={Link}
      />
    </LegalPageLayout>
  );
}
