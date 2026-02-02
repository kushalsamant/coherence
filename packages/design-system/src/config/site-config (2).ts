export interface NavLink {
  href: string
  label: string
}

export interface FooterLink {
  href: string
  label: string
}

export interface SocialLink {
  href: string
  label: string
}

export interface BrandColors {
  primary: string
  secondary: string
  gradientFrom?: string
  gradientTo?: string
}

export interface SiteConfig {
  name: string
  domain: string
  brandColors: BrandColors
  navigation: NavLink[]
  footer?: {
    legalLinks?: FooterLink[]
    socialLinks?: SocialLink[]
    branding?: string
  }
}

export function createSiteConfig(config: Partial<SiteConfig> & { name: string; domain: string; brandColors: BrandColors }): SiteConfig {
  return {
    name: config.name,
    domain: config.domain,
    brandColors: {
      primary: config.brandColors.primary,
      secondary: config.brandColors.secondary,
      gradientFrom: config.brandColors.gradientFrom || config.brandColors.primary,
      gradientTo: config.brandColors.gradientTo || config.brandColors.secondary,
    },
    navigation: config.navigation || [],
    footer: config.footer || {},
  }
}

