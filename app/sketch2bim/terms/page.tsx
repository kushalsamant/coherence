import Link from 'next/link';
import { LegalPageLayout, TermsPage, AppFooter } from '@kushalsamant/design-template';

export const metadata = {
  title: 'Terms and Conditions - Sketch-to-BIM',
  description: 'Terms and Conditions for Sketch-to-BIM service',
};

export default function TermsPageWrapper() {
  return (
    <LegalPageLayout
      title="Terms and Conditions"
      appName="Sketch-to-BIM"
      homeLink="/"
      lastUpdated={new Date()}
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
      <TermsPage
        appName="Sketch-to-BIM"
        serviceDescription="web-based service that converts architectural sketches into Building Information Modeling (BIM) files"
        LinkComponent={Link}
      />
    </LegalPageLayout>
  );

}

