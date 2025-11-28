<!-- d85d6f6d-4d0e-4455-a38b-05ed99871771 eb996359-22db-43e5-8d14-ca8367043530 -->
# Update Design Template in All Repositories

## Overview

Update all repositories in `C:\Users\mital\OneDrive\Documents\GitHub` that use `@kushalsamant/design-template` to use the updated AppFooter with kvshvl.in link support and legal page components.

## Repositories Found

1. **sketch2bim** - Already updated ✅
2. **kushalsamant.github.io** - Needs update
3. **reframe** - Needs update

## Changes to Apply to Each Repository

### 1. Update Footer Components

- Replace custom footers with `AppFooter` from design template
- Add `companyLink="https://kvshvl.in"` and `companyLabel="KVSHVL"` props
- Pass appropriate `legalLinks` array

### 2. Update Legal Pages (if they exist)

- Replace custom legal pages with `LegalPageLayout` wrapper
- Use legal page components (TermsPage, PrivacyPage, RefundPage, ShippingPage, ContactPage) from design template
- Pass appropriate props (appName, homeLink, etc.)

### 3. Ensure Design Template Version

- Verify all repos are using the same version or latest version of `@kushalsamant/design-template`
- If needed, update package.json to use latest version

## Implementation Steps

### For each repository:

1. Check current footer implementation
2. Check if legal pages exist
3. Update footer to use AppFooter component
4. Update legal pages to use design template components
5. Verify imports and LinkComponent props
6. Test that everything works correctly

## Files to Check/Update in Each Repo

### Common patterns:

- `app/page.tsx` or `pages/index.tsx` - Main page footer
- `app/*/page.tsx` - Individual page footers
- `app/terms/page.tsx` or `pages/terms.tsx` - Terms page
- `app/privacy/page.tsx` or `pages/privacy.tsx` - Privacy page
- `app/refund/page.tsx` or `pages/refund.tsx` - Refund page
- `app/shipping/page.tsx` or `pages/shipping.tsx` - Shipping page
- `app/contact/page.tsx` or `pages/contact.tsx` - Contact page

### Pattern to look for:

- Custom footer markup (footer tags, nav elements)
- Custom legal page layouts
- Direct use of kvshvl.in links in footers

### To-dos

- [x] 