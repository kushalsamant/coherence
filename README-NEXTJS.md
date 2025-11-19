# Next.js Migration - kushalsamant.github.io

This repository is being migrated from Jekyll to Next.js.

## Current Status

✅ Next.js project initialized
✅ TypeScript configured
✅ Markdown processing utilities created
✅ Blog post routing setup
✅ Basic components created
⏳ Installation in progress
⏳ Pages migration in progress
⏳ Styling migration pending
⏳ Deployment pending

## Setup

1. Install dependencies:
```bash
npm install
```

2. Run development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

4. Start production server:
```bash
npm start
```

## Structure

- `app/` - Next.js App Router pages and layouts
- `components/` - React components
- `lib/` - Utilities (markdown processing, etc.)
- `anthology/` - Blog posts (296 markdown files) - unchanged
- `assets/` - Static assets (images, fonts) - unchanged
- `_sass/` - SCSS files (to be migrated to CSS Modules)

## Migration Progress

- [x] Project setup
- [x] Markdown utilities
- [x] Blog routing
- [x] Basic components
- [ ] All pages migrated
- [ ] Styling migrated
- [ ] SEO configured
- [ ] Deployed to Vercel

## Notes

- All markdown files in `anthology/` are preserved
- Static assets remain in `assets/`
- Jekyll files will be removed after migration complete
