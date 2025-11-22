import Link from 'next/link'
import { AppFooter } from '@kushalsamant/design-template'

const legalLinks = [
  { href: 'https://kvshvl.in/privacypolicy', label: 'Privacy Policy' },
  { href: 'https://kvshvl.in/termsofservice', label: 'Terms of Service' },
  { href: 'https://kvshvl.in/cancellationrefund', label: 'Cancellation & Refund' },
  { href: 'https://kvshvl.in/getintouch', label: 'Get in Touch' },
]

const productLinks = [
  { href: 'https://sketch2bim.kvshvl.in', label: 'Sketch2BIM' },
  { href: 'https://ask.kvshvl.in', label: 'Ask' },
  { href: 'https://reframe.kvshvl.in', label: 'Reframe' },
]

const socialLinks = [
  { href: 'https://github.com/kushalsamant', label: 'GitHub' },
  { href: 'https://linkedin.com/in/kvshvl', label: 'LinkedIn' },
  { href: 'https://kvshvl.medium.com', label: 'Medium' },
  { href: 'https://instagram.com/kvshvl', label: 'Instagram' },
  { href: 'https://twitter.com/kvshvl_', label: 'Twitter' },
  { href: 'https://youtube.com/@kvshvl', label: 'YouTube' },
]

export default function FooterWrapper() {
  const currentYear = new Date().getFullYear()
  
  return (
    <AppFooter
      legalLinks={legalLinks}
      productLinks={productLinks}
      socialLinks={socialLinks}
      branding={`© ${currentYear} Architect Kushal Dhananjay Samant. Licensed under the Architect's Act, 1972 of India.`}
      companyLink="https://kvshvl.in"
      companyLabel="KVSHVL"
      LinkComponent={Link}
    />
  )
}

