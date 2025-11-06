# Technical Reference

Comprehensive technical documentation for the KVSHVL website architecture, configuration, and deployment.

---

## Repository Structure

```
kushalsamant.github.io/
├── _config.yml                          # Jekyll configuration
├── _layouts/                            # HTML layout templates
│   ├── default.html                     # Main site layout
│   └── post.html                        # Blog post layout
├── _sass/                               # SCSS stylesheets
│   ├── fonts.scss                       # Typography definitions
│   ├── portfolio-dark-theme.scss        # Dark minimalist theme
│   └── rouge-github.scss                # Code syntax highlighting
├── _includes/                           # Reusable components
│   └── youtube_embed.html
├── assets/                              # Static assets
│   ├── css/                            # Compiled CSS
│   ├── fonts/                          # Font files
│   ├── img/                            # Images (115 files including favicon.svg)
│   └── js/
│       └── slideshow.js                # Swiper carousel configuration
├── anthology/                           # 296 blog posts
├── projects/                            # Portfolio project pages
├── marketing/                           # SEO and marketing
│   ├── rss.xml                         # RSS feed
│   └── sitemap/                        # XML sitemaps (1144 files)
├── .github/                             # GitHub configuration
│   ├── .workflows/                      # CI/CD workflows (hidden subdirectory)
│   │   ├── update_rss.yml
│   │   └── update_sitemap.yml
│   ├── business.md                      # Business information
│   ├── design-system.md                 # Design documentation
│   ├── implementation.md                # Implementation history
│   ├── legal-compliance.md              # Legal documentation
│   ├── production-status.md             # Production status
│   ├── setup.md                         # Setup guide
│   ├── testing.md                       # Testing guidelines
│   └── technical.md                     # This file
│
├── Core Pages:
├── index.md                            # Homepage (SVMVNT)
├── about.md                            # Professional biography
├── people.md                           # Acknowledgments (132 people)
├── projects.md                         # Portfolio index
├── anthology.md                        # Blog index
├── support.md                          # Business contact & services
├── contact.md                          # Personal contact page
│
├── Legal Documentation:
├── termsofservice.md                   # Terms of Service (748 lines)
├── privacypolicy.md                    # Privacy Policy (915 lines)
├── cancellationandrefundpolicy.md      # Refund Policy (638 lines)
│
└── Configuration Files:
    ├── CNAME                           # Custom domain (kvshvl.in)
    ├── Gemfile                         # Ruby dependencies
    ├── jekyll-theme-minimal.gemspec    # Theme specification
    └── LICENSE                         # License information
```

---

## Tech Stack

| Component | Technology | Version/Details |
|-----------|------------|-----------------|
| **Static Site Generator** | Jekyll | 4.x |
| **Hosting** | GitHub Pages | Automatic deployment |
| **Domain** | kvshvl.in | Custom domain with HTTPS |
| **Styling** | SCSS/CSS | Dark minimalist theme |
| **Typography** | Times New Roman serif | Elegant serif with tight kerning |
| **Carousel** | Swiper.js 11.x | Fade transitions, auto-advance |
| **Analytics** | Google Analytics 4 | G-0LNSC1VBGQ |
| **Tag Management** | Google Tag Manager | GTM-KXDZLM4W |
| **Booking System** | Setmore | kvshvl.setmore.com |
| **CI/CD** | GitHub Actions | RSS, sitemap generation |
| **Version Control** | Git / GitHub | Main branch deployment |
| **Content Format** | Markdown | .md files |

---

## Jekyll Configuration

### _config.yml

**Core Settings:**
```yaml
title: KVSHVL
description: Official Site / KVSHVL
author: Kushal Samant
email: kushaldsamant@gmail.com
theme: jekyll-theme-minimal
```

**Plugins:**
- `jekyll-feed` - RSS feed generation
- `jekyll-seo-tag` - SEO meta tags

**Social Links:**
- GitHub: kushalsamant
- Instagram: kvshvl
- LinkedIn: kvshvl
- Twitter: kvshvl_
- YouTube: kvshvl

**Build Settings:**
```yaml
markdown: kramdown
kramdown:
  input: GFM
  syntax_highlighter: rouge
```

---

## Analytics & Tracking

### Google Analytics 4

**Property ID:** G-0LNSC1VBGQ

**Setup:**
- Implemented in `_layouts/default.html`
- Tracks page views automatically
- Custom events configured
- Real-time reporting enabled

**Data Collection:**
- Page views
- User sessions
- Geographic location
- Device types
- Traffic sources
- User engagement

### Google Tag Manager

**Container ID:** GTM-KXDZLM4W

**Implementation:**
- Head injection in default layout
- Body injection in default layout
- Custom event tracking
- Tag firing on page load

**Tags Configured:**
- Google Analytics 4
- Custom tracking events
- Conversion tracking (if applicable)

### Legacy Analytics

**Universal Analytics:** UA-105795582-1 (configured in _config.yml, deprecated)

---

## SEO & Meta Tags

### Meta Description

```html
<meta name="description" content="Official Site / Kushal Samant">
```

### Meta Keywords

Comprehensive list covering:
- Architecture
- CSS, HTML, JavaScript
- Design, Development
- Portfolio, Projects
- SaaS, Software Development

### Meta Author

```html
<meta name="author" content="Kushal Samant">
```

### Open Graph Tags

```html
<meta property="og:title" content="KVSHVL">
<meta property="og:description" content="Official Site">
<meta property="og:image" content="[preview image]">
<meta property="og:url" content="https://kvshvl.in">
```

### Twitter Card Tags

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@kvshvl_">
```

### Viewport Configuration

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### Additional Meta

- Pinterest domain verification
- Smooth scrolling enabled
- Responsive design configured

---

## Layout & Design

### Default Layout Structure

```html
<!DOCTYPE html>
<html lang="en-US">
  <head>
    <!-- Meta tags -->
    <!-- Stylesheets -->
    <!-- Analytics -->
  </head>
  <body>
    <!-- GTM noscript -->
    <header>
      <!-- Navigation -->
    </header>
    <section>
      <!-- Page content -->
    </section>
    <footer>
      <!-- Legal links -->
      <!-- Social links -->
    </footer>
  </body>
</html>
```

### Post Layout

Extends default layout with:
- Post metadata
- Author information
- Date display
- Reading time (if configured)

### CSS/SCSS Architecture

**Main Stylesheet:** `assets/css/style.scss`

**SCSS Imports:**
```scss
@import "fonts";
@import "jekyll-theme-minimal-modern-architecture";
@import "rouge-github";
```

For design details, see [Design System](.github/design-system.md).

### Typography

**Font Family:** Noto Sans

**Variants:**
- Regular (400)
- Italic (400)
- Bold (700)
- Bold Italic (700)

**Formats:** EOT, SVG, TTF, WOFF, WOFF2

**Font Files:** 20 total (5 per variant x 4 variants)

---

## GitHub Actions Workflows

### Update RSS Feed

**File:** `.github/.workflows/update_rss.yml`

**Trigger:**
- Push to main branch
- Manual workflow dispatch

**Actions:**
- Generate RSS feed from blog posts
- Update `marketing/rss.xml`
- Commit changes (if any)

### Update Sitemap

**File:** `.github/.workflows/update_sitemap.yml`

**Trigger:**
- Push to main branch
- Manual workflow dispatch

**Actions:**
- Generate sitemap for all pages
- Update `marketing/sitemap/` files
- Include all 321 markdown files
- Commit changes (if any)

---

## Deployment Process

### Automatic Deployment (GitHub Pages)

**Flow:**
1. Developer pushes to `main` branch
2. GitHub Actions workflows run
3. GitHub Pages builds site with Jekyll
4. Site deployed to https://kushalsamant.github.io
5. Custom domain (kvshvl.in) serves the site

**Build Configuration:**
- Source: main branch, root directory
- Jekyll version: GitHub Pages default
- Custom domain: Configured via CNAME file
- HTTPS: Enforced automatically

### Custom Domain Setup

**CNAME File:**
```
kvshvl.in
```

**DNS Configuration:**
- A records pointing to GitHub Pages IPs
- CNAME record for www subdomain (optional)
- SSL/TLS certificate (automatic via GitHub)

**Verification:**
- Domain verified in GitHub Settings
- HTTPS redirect enabled
- Certificate valid and auto-renewing

---

## File Organization

### Content Files

**Main Pages:** Root directory (`.md` files)  
**Blog Posts:** `anthology/` (296 files)  
**Projects:** `projects/` subdirectories  
**Legal Docs:** Root directory (`*policy.md`, `termsofservice.md`)

### Asset Organization

**CSS:** `assets/css/`  
**Fonts:** `assets/fonts/` (organized by variant)  
**Images:** `assets/img/` (115 files)  
**JavaScript:** `assets/js/` (slideshow.js - Swiper carousel configuration)

### Documentation

**Repository Docs:** `.github/` (8 documentation files)  
**Workflows:** `.github/.workflows/` (2 automation files - hidden subdirectory)

---

## Performance Optimization

### Static Site Benefits

- ✅ Pre-generated HTML (no server-side processing)
- ✅ Fast page loads
- ✅ CDN delivery via GitHub Pages
- ✅ Excellent caching
- ✅ Low bandwidth usage

### Asset Optimization

**Images:**
- Optimized file sizes
- Appropriate dimensions
- Modern formats where supported

**CSS:**
- Minified in production
- Single stylesheet
- Critical CSS inlined (if configured)

**JavaScript:**
- Minimal JS usage
- External scripts loaded asynchronously
- Analytics scripts deferred

### Caching Strategy

- Static assets cached by GitHub Pages
- Browser caching enabled
- CDN caching for global distribution

---

## Security

### HTTPS

- ✅ SSL/TLS certificate via GitHub Pages
- ✅ Automatic HTTPS redirect
- ✅ TLS 1.3 support
- ✅ HSTS enabled

### Content Security

- Static site (no server-side vulnerabilities)
- No database (no SQL injection risk)
- No user input processing server-side
- Content validated at build time

### Data Protection

For compliance details, see [Legal & Compliance](.github/legal-compliance.md).

---

## Monitoring & Maintenance

### Analytics Monitoring

- Google Analytics 4 dashboard
- Real-time visitor tracking
- Traffic source analysis
- Conversion tracking

### Performance Monitoring

- Lighthouse audits (regular)
- PageSpeed Insights checks
- Core Web Vitals tracking
- Uptime monitoring (GitHub Pages status)

### Content Updates

**Frequency:**
- Blog posts: As needed
- Project updates: Ongoing
- Legal docs: Annual review recommended
- Design updates: As needed

**Process:**
1. Edit markdown files locally
2. Test with `bundle exec jekyll serve`
3. Commit changes to git
4. Push to main branch
5. Automatic deployment via GitHub Pages

---

## Backup & Recovery

### Version Control

- Full repository history in Git
- All changes tracked
- Easy rollback to previous versions
- Branches for experimental changes

### GitHub Archive

- Repository selected for GitHub Archive Program (2020)
- Arctic Code Vault preservation
- Long-term archival

---

## Browser Support

### Fully Supported

- Chrome 88+
- Firefox 85+
- Safari 14+
- Edge 88+

### CSS Features Used

- CSS Custom Properties
- CSS Grid
- Flexbox
- Backdrop Filter
- Container Queries (progressive enhancement)

### Graceful Degradation

- Core content accessible on all browsers
- Enhanced features for modern browsers
- Fallbacks for older browsers

---

## Development Tools

### Recommended IDE

- Visual Studio Code
- Atom
- Sublime Text
- Vim/Neovim

### Useful Extensions

**VS Code:**
- Markdown All in One
- SCSS IntelliSense
- Liquid (Shopify Liquid syntax)
- GitLens

### Testing Tools

- Chrome DevTools
- Firefox Developer Tools
- Lighthouse
- PageSpeed Insights

For complete testing guidelines, see [Testing](.github/testing.md).

---

## Related Documentation

- **Setup Guide:** See [Setup](.github/setup.md)
- **Design System:** See [Design System](.github/design-system.md)
- **Business Information:** See [Business](.github/business.md)
- **Testing Guidelines:** See [Testing](.github/testing.md)

---

**Last Updated:** November 5, 2025  
**Status:** Complete Technical Reference

