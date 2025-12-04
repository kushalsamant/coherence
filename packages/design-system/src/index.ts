// Main entry point for the design template package

// Components
export { default as Button } from './components/Button'
export { default as Card } from './components/Card'
export { default as Hero } from './components/Hero'
export { default as ProjectCard } from './components/ProjectCard'
export { default as StatsDisplay } from './components/StatsDisplay'
export { default as Testimonial } from './components/Testimonial'
export { default as NewsCard } from './components/NewsCard'
export { default as ClientGrid } from './components/ClientGrid'
export { default as AppHeader } from './components/AppHeader'
export { default as AppFooter } from './components/AppFooter'
export { default as ThemeToggle } from './components/ThemeToggle'
export { default as ThemeProvider } from './components/ThemeProvider'
export { default as Section } from './components/Section'
export { default as LegalPageLayout } from './components/LegalPageLayout'
export { default as TermsPage } from './components/legal/TermsPage'
export { default as PrivacyPage } from './components/legal/PrivacyPage'
export { default as RefundPage } from './components/legal/RefundPage'
export { default as ShippingPage } from './components/legal/ShippingPage'
export { default as ContactPage } from './components/legal/ContactPage'

// Utilities
export * from './lib/theme'
export { initScrollAnimations } from './lib/scroll-animations'
export { buildStandardNavLinks, type BuildStandardNavLinksOptions } from './lib/build-standard-nav-links'

// Configuration
export { createSiteConfig, type SiteConfig } from './config/site-config'

// Types
export type { NavLink } from './components/AppHeader'

// Layout
export { AppLayout } from './components/AppLayout'
export type { AppLayoutProps, LegalLink, SocialLink } from './components/AppLayoutProps'