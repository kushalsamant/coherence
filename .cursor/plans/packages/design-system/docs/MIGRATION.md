# Migration Guide

Guide for migrating existing projects to use the KVSHVL Design Template.

## Installation

### Option 1: npm Package (Recommended)

```bash
npm install @kvshvl/design-template
```

### Option 2: From Monorepo (Development)

```bash
git clone https://github.com/kushalsamant/kushalsamant.github.io.git
cd kushalsamant.github.io/packages/design-system
```

## Step 1: Import Styles

Add the design system CSS to your app:

**Next.js (app directory):**
```typescript
// app/layout.tsx
import '@kvshvl/design-template/styles/globals.css'
```

**Next.js (pages directory):**
```typescript
// pages/_app.tsx
import '@kvshvl/design-template/styles/globals.css'
```

## Step 2: Setup Theme Provider

Wrap your app with ThemeProvider:

```typescript
// app/layout.tsx or _app.tsx
import { ThemeProvider } from '@kvshvl/design-template'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

## Step 3: Replace Components

### Replace Header

**Before:**
```typescript
import AppHeader from '@/components/AppHeader'
```

**After:**
```typescript
import { AppHeader } from '@kvshvl/design-template'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navLinks = [
  { href: '/about', label: 'About' },
  { href: '/projects', label: 'Projects' },
]

<AppHeader
  siteName="Your Site"
  navLinks={navLinks}
  currentPath={usePathname()}
  LinkComponent={Link}
/>
```

### Replace Footer

**Before:**
```typescript
import AppFooter from '@/components/AppFooter'
```

**After:**
```typescript
import { AppFooter } from '@kvshvl/design-template'

<AppFooter
  legalLinks={[
    { href: '/privacy', label: 'Privacy Policy' },
  ]}
  branding="© {year} Your Company"
  LinkComponent={Link}
/>
```

### Replace Buttons

**Before:**
```typescript
import Button from '@/components/Button'
```

**After:**
```typescript
import { Button } from '@kvshvl/design-template'

<Button variant="primary" href="/action" LinkComponent={Link}>
  Click Me
</Button>
```

## Step 4: Configure Site

Create a site configuration:

```typescript
// config/site.config.ts
import { createSiteConfig } from '@kvshvl/design-template'

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
  footer: {
    legalLinks: [
      { href: '/privacy', label: 'Privacy Policy' },
    ],
    branding: '© {year} Your Company',
  },
})
```

## Step 5: Customize Colors (Optional)

Override CSS variables in your global CSS:

```css
:root {
  --color-kvshvl-primary: #your-color;
  --color-kvshvl-secondary: #your-color;
}
```

## Step 6: Remove Old Components

Once migrated, remove old component files:
- `components/Button.tsx`
- `components/Card.tsx`
- `components/AppHeader.tsx`
- `components/AppFooter.tsx`
- `components/ThemeToggle.tsx`
- `components/ThemeProvider.tsx`
- `lib/theme.ts`
- `lib/scroll-animations.ts`

## Automatic Updates

### npm Package

Update the package:
```bash
npm update @kvshvl/design-template
```

Set up automated updates with Dependabot (`.github/dependabot.yml`):
```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Git Submodule

Update submodule:
```bash
git submodule update --remote
git add template
git commit -m "Update design template"
```

## Troubleshooting

### TypeScript Errors

Ensure you have the correct TypeScript types:
```bash
npm install --save-dev @types/react @types/react-dom
```

### Styling Issues

Make sure you've imported the CSS file:
```typescript
import '@kvshvl/design-template/styles/globals.css'
```

### Link Component Issues

Always pass your router's Link component:
```typescript
import Link from 'next/link' // or your router's Link

<AppHeader LinkComponent={Link} />
```

## Next Steps

- Review [Component Documentation](./COMPONENTS.md)
- Check [Design System Guide](./DESIGN_SYSTEM.md)
- Customize colors and spacing as needed

