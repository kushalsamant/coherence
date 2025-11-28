import Link from 'next/link';
import { LegalPageLayout, ShippingPage, AppFooter } from '@kushalsamant/design-template';

export const metadata = {
  title: 'Shipping and Exchange Policy - Sketch-to-BIM',
  description: 'Shipping and Exchange Policy for Sketch-to-BIM service',
};

export default function ShippingPageWrapper() {
  return (
    <LegalPageLayout
      title="Shipping and Exchange Policy"
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
      <ShippingPage LinkComponent={Link} />
    </LegalPageLayout>
  );
}
