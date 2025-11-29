# Component Documentation

Complete API documentation for all components in the KVSHVL Design Template.

## Layout Components

### AppHeader

Sticky header with navigation and theme toggle.

```typescript
<AppHeader
  siteName="KVSHVL"
  siteNameHref="/"
  navLinks={[
    { href: '/about', label: 'About' },
    { href: '/projects', label: 'Projects' },
  ]}
  currentPath={pathname}
  LinkComponent={Link} // Next.js Link or your router's Link
/>
```

**Props:**
- `siteName?: string` - Site name/brand (default: 'KVSHVL')
- `siteNameHref?: string` - Home link (default: '/')
- `navLinks?: NavLink[]` - Navigation links
- `currentPath?: string` - Current pathname for active state
- `LinkComponent?: React.ComponentType` - Custom Link component (e.g., Next.js Link)
- `onNavClick?: (href: string) => void` - Navigation click handler

### AppFooter

Footer with organized links and branding.

```typescript
<AppFooter
  legalLinks={[
    { href: '/privacy', label: 'Privacy Policy' },
  ]}
  socialLinks={[
    { href: 'https://twitter.com', label: 'Twitter' },
  ]}
  branding="© {year} Your Company"
  LinkComponent={Link}
/>
```

**Props:**
- `legalLinks?: FooterLink[]` - Legal/utility links
- `socialLinks?: SocialLink[]` - Social media links
- `branding?: string` - Footer branding text (use {year} for current year)
- `LinkComponent?: React.ComponentType` - Custom Link component

### ThemeProvider

Initializes theme and scroll animations. Wrap your app with this.

```typescript
<ThemeProvider>
  {children}
</ThemeProvider>
```

## Content Components

### Hero

Large hero section with title, tagline, and CTA.

```typescript
<Hero
  title="Welcome to KVSHVL"
  tagline="Supporting tagline text"
  description="Optional longer description"
  cta={{
    label: 'Get Started',
    href: '/start',
    variant: 'primary',
  }}
  LinkComponent={Link}
/>
```

**Props:**
- `title: string` - Main headline
- `tagline?: string` - Supporting tagline
- `description?: string` - Longer description
- `cta?: { label: string; href?: string; onClick?: () => void; variant?: 'primary' | 'secondary' | 'ghost' }` - Call to action
- `LinkComponent?: React.ComponentType` - Custom Link component

### ProjectCard

Project/product showcase card.

```typescript
<ProjectCard
  title="Project Name"
  description="Project description"
  image="/project.jpg"
  imageAlt="Project screenshot"
  href="/projects/project"
  tags={['React', 'TypeScript']}
  date="2024"
  LinkComponent={Link}
/>
```

**Props:**
- `title: string` - Project title
- `description: string` - Project description
- `image?: string` - Project image URL
- `imageAlt?: string` - Image alt text
- `href?: string` - Link to project
- `tags?: string[]` - Project tags
- `date?: string` - Project date
- `LinkComponent?: React.ComponentType` - Custom Link component

### StatsDisplay

Prominent statistics/metrics display.

```typescript
<StatsDisplay
  stats={[
    { value: '100+', label: 'Projects', description: 'Completed' },
    { value: '50+', label: 'Clients', description: 'Satisfied' },
  ]}
  columns={3}
/>
```

**Props:**
- `stats: Stat[]` - Array of statistics
- `columns?: 2 | 3 | 4` - Number of columns (default: 3)

### Testimonial

Quote/testimonial block.

```typescript
<Testimonial
  quote="This is an amazing service!"
  author="John Doe"
  role="CEO"
  company="Company Inc."
/>
```

**Props:**
- `quote: string | ReactNode` - Testimonial quote
- `author: string` - Author name
- `role?: string` - Author role
- `company?: string` - Company name

### NewsCard

Blog/news article card.

```typescript
<NewsCard
  title="Article Title"
  description="Article description"
  image="/article.jpg"
  href="/news/article"
  category="News"
  date="2024-01-01"
  LinkComponent={Link}
/>
```

**Props:**
- `title: string` - Article title
- `description?: string` - Article description
- `image?: string` - Article image
- `imageAlt?: string` - Image alt text
- `href?: string` - Link to article
- `category?: string` - Article category
- `date?: string` - Publication date
- `LinkComponent?: React.ComponentType` - Custom Link component

### ClientGrid

Client/product logo grid.

```typescript
<ClientGrid
  clients={[
    { name: 'Client 1', logo: '/logo1.png', href: '/clients/1' },
    { name: 'Client 2', logo: '/logo2.png' },
  ]}
  columns={4}
  LinkComponent={Link}
/>
```

**Props:**
- `clients: Client[]` - Array of clients
- `columns?: 3 | 4 | 5 | 6` - Number of columns (default: 4)
- `LinkComponent?: React.ComponentType` - Custom Link component

## Utility Components

### Button

Button with multiple variants.

```typescript
<Button
  variant="primary"
  size="lg"
  href="/action"
  onClick={() => {}}
  LinkComponent={Link}
>
  Click Me
</Button>
```

**Props:**
- `children: ReactNode` - Button content
- `variant?: 'primary' | 'secondary' | 'ghost'` - Button style
- `size?: 'sm' | 'md' | 'lg'` - Button size
- `href?: string` - Link URL (renders as link)
- `onClick?: () => void` - Click handler
- `disabled?: boolean` - Disabled state
- `LinkComponent?: React.ComponentType` - Custom Link component

### Card

General purpose card component.

```typescript
<Card variant="elevated" hover onClick={() => {}}>
  Card content
</Card>
```

**Props:**
- `children: ReactNode` - Card content
- `variant?: 'default' | 'elevated' | 'outlined'` - Card style
- `hover?: boolean` - Enable hover effects
- `onClick?: () => void` - Click handler (makes card interactive)

### Section

Section wrapper with consistent spacing.

```typescript
<Section id="about" className="custom-class">
  Section content
</Section>
```

**Props:**
- `children: ReactNode` - Section content
- `className?: string` - Additional CSS classes
- `id?: string` - Section ID

### ThemeToggle

Dark/light/system theme toggle.

```typescript
<ThemeToggle />
```

No props required. Automatically handles theme switching.

