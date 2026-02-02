import type { NavLink } from '../components/AppHeader'

export interface BuildStandardNavLinksOptions {
  isSignedIn: boolean
  pricingHref?: string
  dashboardHref?: string
  signInHref?: string
  signOutHref?: string
}

/**
 * Builds standard navigation links for product sites.
 * Returns: Pricing (always), Dashboard (when signed in), Sign In/Sign Out (conditional)
 */
export function buildStandardNavLinks(options: BuildStandardNavLinksOptions): NavLink[] {
  const {
    isSignedIn,
    pricingHref = '/pricing',
    dashboardHref = '/dashboard',
    signInHref = '/api/auth/signin',
    signOutHref = '/api/auth/signout',
  } = options

  const links: NavLink[] = []

  // Pricing is always visible
  links.push({ href: pricingHref, label: 'Pricing' })

  // Dashboard only when signed in
  if (isSignedIn) {
    links.push({ href: dashboardHref, label: 'Dashboard' })
  }

  // Sign In when not signed in, Sign Out when signed in
  if (isSignedIn) {
    links.push({ href: signOutHref, label: 'Sign Out' })
  } else {
    links.push({ href: signInHref, label: 'Sign In' })
  }

  return links
}

