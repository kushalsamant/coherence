# KVSHVL Design Template

A unified design system and component library based on the Awwwards-winning GKC Architecture & Design pattern. This template provides a consistent, professional design language for all KVSHVL projects.

## Features

- **Minimal, Clean Aesthetic** - Professional design with maximum impact
- **Dark Mode Support** - System preference detection with manual toggle
- **Responsive Design** - Mobile-first approach with excellent mobile experience
- **Accessibility** - WCAG AAA compliant
- **Performance** - Optimized animations and 60fps performance
- **Type-Safe** - Full TypeScript support

## Installation

### As npm Package

```bash
npm install @kvshvl/design-template
```

### From Monorepo

The design system is part of the `kushalsamant.github.io` monorepo:

```bash
git clone https://github.com/kushalsamant/kushalsamant.github.io.git
cd kushalsamant.github.io/packages/design-system
```

## Quick Start

### 1. Install the Package

```bash
npm install @kvshvl/design-template
```

### 2. Import Styles

```typescript
// app/layout.tsx or _app.tsx
import '@kvshvl/design-template/styles/globals.css'
```

### 3. Configure Your Site

```typescript
// config/site.config.ts
import { createSiteConfig } from '@kvshvl/design-template/config'

export const siteConfig = createSiteConfig({
  name: 'Your Site Name',
  domain: 'yoursite.com',
  brandColors: {
    primary: '#9333EA',
    secondary: '#EC4899',
  },
  navigation: [
    { href: '/about', label: 'About' },
    { href: '/projects', label: 'Projects' },
  ],
})
```

### 4. Use Components

```typescript
import { Hero, ProjectCard, Button } from '@kvshvl/design-template/components'

export default function Home() {
  return (
    <>
      <Hero
        title="Your Site Title"
        tagline="Supporting tagline"
        cta={{ label: 'Get Started', href: '/start' }}
      />
      <ProjectCard
        title="Project Name"
        description="Project description"
        image="/project.jpg"
        href="/projects/project"
      />
    </>
  )
}
```

## Components

### Layout Components

- `AppHeader` - Sticky header with navigation and theme toggle
- `AppFooter` - Footer with organized links and branding
- `ThemeProvider` - Theme initialization and scroll animations

### Content Components

- `Hero` - Large hero section with title, tagline, and CTA
- `ProjectCard` - Project/product showcase card
- `Card` - General purpose card component
- `Button` - Button with multiple variants
- `StatsDisplay` - Statistics/metrics display
- `Testimonial` - Quote/testimonial block
- `NewsCard` - Blog/news article card
- `ClientGrid` - Client/product logo grid

### Utility Components

- `ThemeToggle` - Dark/light/system theme toggle
- `Section` - Section wrapper with consistent spacing

## Design System

### Typography

- **Font Family**: Inter (Google Fonts)
- **Headings**: H1 (4rem-5rem), H2 (3rem-4rem), H3 (1.875rem)
- **Body**: 1rem base size with relaxed line-height

### Colors

- **Primary**: #9333EA (Purple)
- **Secondary**: #EC4899 (Pink)
- **Gradient**: Primary to Secondary
- Full dark mode support with system preference detection

### Spacing

- Generous spacing system: xs (8px) to 3xl (64px)
- Section spacing: 4rem-6rem between major sections

### Animations

- Smooth transitions (150ms-500ms)
- Scroll-triggered animations
- Hover effects with elevation changes
- Respects `prefers-reduced-motion`

## Configuration

See [CONFIGURATION.md](./docs/CONFIGURATION.md) for detailed configuration options.

## Documentation

- [Components](./docs/COMPONENTS.md) - Complete component API
- [Design System](./docs/DESIGN_SYSTEM.md) - Design tokens and patterns
- [Migration Guide](./docs/MIGRATION.md) - Migrating existing projects

## Automatic Updates

This template is designed to automatically update across all projects:

### npm Package Method

1. Update design system in monorepo (`packages/design-system/`)
2. Publish new version: `npm version patch && npm publish`
3. Projects update: `npm update @kushalsamant/design-template`
4. Automated via Dependabot/Renovate

### Monorepo Method

1. Update design system in monorepo (`packages/design-system/`)
2. Publish new version: `npm version patch && npm publish`
3. Projects update: `npm update @kushalsamant/design-template`

## License

See [LICENSE](./LICENSE) file for details.

## Support

For issues and questions, please open an issue in the [monorepo](https://github.com/kushalsamant/kushalsamant.github.io).

