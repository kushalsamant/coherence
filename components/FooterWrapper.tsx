import Link from 'next/link'
import { AppFooter } from '@kushalsamant/design-template'

const legalLinks = [
  { href: '/privacypolicy', label: 'Privacy Policy' },
  { href: '/termsofservice', label: 'Terms of Service' },
  { href: '/cancellationrefund', label: 'Cancellation & Refund' },
]

export default function FooterWrapper() {
  const currentYear = new Date().getFullYear()
  
  return (
    <AppFooter
      legalLinks={legalLinks}
      branding={`© ${currentYear} Architect Kushal Dhananjay Samant. Licensed under the Architect's Act, 1972 of India.`}
      companyLink="https://kvshvl.in"
      companyLabel="KVSHVL"
      LinkComponent={Link}
    />
  )
}

