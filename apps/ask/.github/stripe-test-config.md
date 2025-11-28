# Stripe Test Configuration

Generated: 6/11/2025, 4:20:28 pm
Mode: **TEST**

## Subscription Products

### Weekly Pro - $2.99/week
- Product ID: `prod_TNB8PjrJrwL03o`
- Price ID: `price_1SQQllJlfVCbQ3BNg9wCWxS8`
- Description: 50 requests per week with all character limits unlocked

### Monthly Pro - $9.99/month
- Product ID: `prod_TNB8gtkaeSQ6QC`
- Price ID: `price_1SQQllJlfVCbQ3BNUULfpge5`
- Description: Unlimited requests with all character limits unlocked

### Yearly Pro - $99/year
- Product ID: `prod_TNB8UxNnNC5RFR`
- Price ID: `price_1SQQlmJlfVCbQ3BNvHzVJrKY`
- Description: Unlimited requests with all character limits unlocked (Save 17%!)

## Credit Pack Products

### Starter Pack - $3.99 (10 credits)
- Product ID: `prod_TNB8tRTwvE9E3O`
- Price ID: `price_1SQQlnJlfVCbQ3BNOy8dUj7f`
- Description: Perfect for 1-2 documents

### Standard Pack - $9.99 (30 credits)
- Product ID: `prod_TNB8lFGPrJobQK`
- Price ID: `price_1SQQlnJlfVCbQ3BN7RSMWezK`
- Description: Best for occasional use

### Premium Pack - $24.99 (100 credits)
- Product ID: `prod_TNB80NkHdlTcju`
- Price ID: `price_1SQQloJlfVCbQ3BNNodFNOjp`
- Description: Bulk one-time projects

## Configuration Files

**All price IDs are now stored in:**
- `config/stripe.test.json` - Test mode prices (USD + INR)
- `config/stripe.production.json` - Production prices (USD + INR)

**Note:** Price IDs are no longer in `.env.local` - they've been migrated to JSON config files for better organization.

## Testing

Use these test cards in Stripe test mode:
- **Success**: `4242 4242 4242 4242`
- **Decline**: `4000 0000 0000 0002`
- **Expired Date**: Any future date
- **CVV**: Any 3 digits

## Dashboard Links

- View Products: https://dashboard.stripe.com/test/products
- View Prices: https://dashboard.stripe.com/test/prices

