# Remove Credit Packs from Reframe

## Issue
Credit packs are documented and referenced in multiple places but are not actually implemented (no API routes, no credit balance tracking, no checkout logic). Need to remove all credit pack references.

## Files to Update

### 1. Components ✅ COMPLETED
- `apps/reframe/components/ui/dual-price-display.tsx` ✅
  - Removed credit_10, credit_30, credit_100 from PRICING object

- `apps/reframe/components/export-data-modal.tsx` ✅
  - Removed "Credit balance" from export data list

- `apps/reframe/components/delete-account-modal.tsx` ✅
  - Removed "Any remaining credits (no refunds)" from deletion warning

### 2. Pages - ✅ COMPLETED
- `apps/reframe/app/page.tsx` ✅
  - Removed "or buy credit packs" text from free limit message

- `apps/reframe/app/terms/page.tsx` ✅
  - Removed credit pack refund policy mention
  - Changed "purchasing credits" to "subscribing"

- `apps/reframe/app/privacy/page.tsx` ✅
  - Changed "or credit pack" to just subscription

- `apps/reframe/app/pricing/layout.tsx` ✅
  - Removed credit pack mentions from metadata descriptions
  - Removed "credit packs" from keywords

### 3. Documentation - ✅ COMPLETED
- `apps/reframe/readme.md` ✅
  - Changed "Credit packs or subscriptions" to "Monthly or yearly subscriptions" in features list
  - Removed entire "Credit Packs (One-Time)" section
  - Removed credit pack from pricing configuration section

### 4. Verify - ✅ COMPLETED
- ✅ Verified no credit pack references remain in the codebase

## Implementation Steps

1. ✅ Remove credit pack pricing from dual-price-display component
2. ✅ Remove credit pack mentions from export/delete modals
3. ✅ Remove credit pack text from home page
4. ✅ Remove credit pack sections from terms page (refund policy)
5. ✅ Remove credit pack mentions from privacy page
6. ✅ Update metadata and SEO descriptions in pricing layout
7. ✅ Remove credit pack sections from readme.md
8. ✅ Verify no credit pack references remain

