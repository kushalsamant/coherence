# Next.js Migration - kushalsamant.github.io

This repository has been migrated from Jekyll to Next.js 14.

## Current Status

✅ Next.js project initialized and configured
✅ TypeScript configured
✅ All pages migrated (home, history, getintouch, links, legal pages)
✅ KVSHVL dark minimalist design system integrated
✅ SEO metadata configured for all pages
✅ Build tested and verified
✅ Code pushed to GitHub
✅ Deployment to Vercel (project connected and configured)
✅ Custom domain kvshvl.in configured
✅ File organization complete (all .md files in /docs)
✅ HTML redirect files removed (old Jekyll redirects)
✅ Duplicate links removed across website
✅ Pinterest verification file kept (pinterest-bdc46.html)

## Setup

### Local Development

1. Install dependencies:
```bash
npm install
```

2. Run development server:
```bash
npm run dev
```

Access the site at: http://localhost:3000

### Production Build

1. Build for production:
```bash
npm run build
```

This generates a static export in the `out/` directory (Next.js static export mode).

2. Preview production build locally:
```bash
npx serve out
```

## Deployment to Vercel

### Current Vercel Configuration

The project is already connected to Vercel with the following settings:

- **Framework Preset:** Next.js (auto-detected)
- **Build Command:** `npm run build`
- **Install Command:** `npm install`
- **Root Directory:** (empty - Next.js in repo root)
- **Node.js Version:** 22.x
- **Build Machine:** Standard (4 vCPUs, 8GB)
- **Output:** Static export (`output: 'export'` in `next.config.js`)

### Deployment Steps

1. **Automatic Deployments**
   - Pushes to `main` branch automatically trigger deployments
   - Check deployment status in Vercel dashboard

2. **Configure Custom Domain**
   - Go to Vercel project settings → Domains
   - Add `kvshvl.in` and `www.kvshvl.in`
   - Configure DNS records at GoDaddy:
     - A record: `@` → Vercel IP addresses (provided in Vercel dashboard)
     - CNAME record: `www` → `cname.vercel-dns.com`
   - SSL certificates are automatically provisioned by Vercel

3. **Verify Deployment**
   - Check all pages load correctly
   - Verify design system renders properly
   - Test all internal links
   - Validate responsive design on mobile/tablet

## Project Structure

- `app/` - Next.js App Router pages and layouts
  - `page.tsx` - Homepage
  - `history/page.tsx` - History page (from history.md)
  - `getintouch/page.tsx` - Get in Touch page
  - `links/page.tsx` - Links page
  - `termsofservice/page.tsx` - Terms of Service
  - `privacypolicy/page.tsx` - Privacy Policy
  - `cancellationrefund/page.tsx` - Cancellation & Refund Policy
- `components/` - React components
  - `AppHeader.tsx` - Site header with navigation
  - `AppFooter.tsx` - Site footer
- `lib/` - Utilities
  - `process-markdown.ts` - Markdown processing for history and legal pages
- `assets/img/` - Static assets (images, logos)
- `history.md`, `termsofservice.md`, `privacypolicy.md`, `cancellationrefund.md` - Source markdown files
- `next.config.js` - Next.js configuration (static export mode)

## Design System

The site uses the KVSHVL dark minimalist design system:
- Pure black background (#000000) with white text
- Times New Roman serif typography
- Large, readable font sizes (26px base)
- Generous whitespace and spacing
- Minimalist aesthetic with subtle borders
- Fully responsive design

## Migration Status

- [x] Project setup
- [x] All pages migrated
- [x] Design system integrated
- [x] SEO metadata configured
- [x] Build tested and verified
- [x] Code pushed to GitHub
- [x] Deployed to Vercel production
- [x] Custom domain configured (kvshvl.in)
- [x] File organization (docs directory)
- [x] Code cleanup (removed duplicates, old redirects)
- [ ] Production verification (test at kvshvl.in)

## Notes

- **Anthology:** Blog posts in `anthology/` directory are preserved but not used by Next.js (moving to Medium)
- **Static Assets:** Images remain in `assets/img/` and are used by Next.js
- **Jekyll Files:** Old Jekyll files (`_config.yml`, `_layouts/`, `_sass/`, etc.) remain in the repository but are not used by Next.js
- **Static Export:** The site is configured for static export, generating static HTML files compatible with any hosting service
- **HTML Redirects:** Old Jekyll redirect files (`about.html`, `people.html`, `projects.html`, `anthology.html`) have been removed. Old URLs will return 404 unless configured in Vercel redirects
- **Pinterest Verification:** `pinterest-bdc46.html` is kept in root for Pinterest domain verification
- **File Organization:** All markdown files (documentation and content) are organized in `/docs` directory
- **Navigation:** Header contains main navigation, footer contains legal links only (no duplicates)
