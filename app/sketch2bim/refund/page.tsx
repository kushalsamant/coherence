import Link from 'next/link';
import { LegalPageLayout, RefundPage, AppFooter } from '@kushalsamant/design-template';

export const metadata = {
  title: 'Cancellation and Refund Policy - Sketch-to-BIM',
  description: 'Cancellation and Refund Policy for Sketch-to-BIM service',
};

export default function RefundPageWrapper() {
  return (
    <LegalPageLayout
      title="Cancellation and Refund Policy"
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
      <RefundPage LinkComponent={Link} />
    </LegalPageLayout>
  );
}
