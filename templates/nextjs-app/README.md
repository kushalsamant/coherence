# Next.js Frontend Template

This template provides a standardized Next.js application structure for KVSHVL platform apps.

## Features

- ✅ Standardized authentication using `@kvshvl/shared-frontend/auth`
- ✅ Unified layout using `AppLayout` component from `@kushalsamant/design-template`
- ✅ Pricing page structure (using shared utilities)
- ✅ Settings page structure (using shared components)
- ✅ TypeScript configuration
- ✅ Path aliases configured (@/*)
- ✅ Standard package dependencies

## Quick Start

1. Copy this template to your new app directory:
   ```bash
   cp -r templates/nextjs-app apps/your-app-name/frontend
   ```

2. Update the app name in:
   - `package.json` - Update name field
   - `auth.ts` - Update appName and URLs
   - `app/layout.tsx` - Update metadata and appName
   - `components/HeaderWrapper.tsx` - Update app-specific navigation

3. Install dependencies:
   ```bash
   cd apps/your-app-name/frontend
   npm install
   ```

4. Set up environment variables (see `.env.template`)

5. Start development:
   ```bash
   npm run dev
   ```

## Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout using AppLayout
│   ├── page.tsx            # Landing page
│   ├── pricing/
│   │   └── page.tsx        # Pricing page (uses shared utilities)
│   └── settings/
│       └── page.tsx        # Settings page (uses shared components)
├── components/
│   └── HeaderWrapper.tsx   # App-specific header component
├── lib/
│   └── api.ts              # API client utilities
├── auth.ts                 # Auth configuration (uses shared auth)
├── package.json
├── tsconfig.json
└── next.config.ts
```

## Customization

- Add app-specific pages in `app/`
- Customize header navigation in `components/HeaderWrapper.tsx`
- Add API routes in `app/api/`
- Configure images/remote patterns in `next.config.ts`

