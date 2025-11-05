# Setup & Development Guide

Complete guide for local development setup, Jekyll installation, and Stripe payment integration.

---

## Prerequisites

### Required Software

**Ruby 2.7 or higher:**
- Install: https://www.ruby-lang.org/en/documentation/installation/
- Verify: `ruby --version`

**Bundler:**
- Install: `gem install bundler`
- Verify: `bundle --version`

**Git:**
- Install: https://git-scm.com/downloads
- Verify: `git --version`

---

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kushalsamant/kushalsamant.github.io.git
cd kushalsamant.github.io
```

### 2. Install Dependencies

```bash
bundle install
```

This will install:
- Jekyll (static site generator)
- jekyll-feed (RSS feed plugin)
- jekyll-seo-tag (SEO optimization)
- Other required gems from `Gemfile`

### 3. Run Development Server

```bash
bundle exec jekyll serve
```

**Access the site:**
- Local URL: http://localhost:4000
- Live reload enabled (changes auto-refresh)

**Options:**
```bash
# Run with drafts
bundle exec jekyll serve --drafts

# Run on different port
bundle exec jekyll serve --port 4001

# Enable incremental builds (faster)
bundle exec jekyll serve --incremental
```

### 4. Build for Production

```bash
bundle exec jekyll build
```

Output will be in the `_site/` directory.

---

## File Structure

### Key Directories

**Root Files:**
- `_config.yml` - Jekyll configuration
- `Gemfile` - Ruby dependencies
- `CNAME` - Custom domain configuration
- `index.md` - Homepage

**Content:**
- `anthology/` - Blog posts (296 files)
- `projects/` - Project pages
- `about.md`, `people.md`, `support.md` - Main pages

**Layouts & Design:**
- `_layouts/` - HTML templates
- `_sass/` - SCSS stylesheets
- `assets/` - CSS, fonts, images, JavaScript

**Documentation:**
- `.github/` - This documentation folder
- `.github/workflows/` - GitHub Actions

For detailed structure, see [Technical Reference](.github/technical.md).

---

## Making Changes

### Content Editing

**Edit markdown files:**
```bash
# Main pages
vim about.md
vim support.md

# Blog posts
vim anthology/your-post.md

# Projects
vim projects/your-project.md
```

**Add new content:**
- Blog posts: Create `.md` file in `anthology/`
- Projects: Create `.md` file in `projects/`
- Pages: Create `.md` file in root

### Layout Modifications

**Edit HTML templates:**
```bash
vim _layouts/default.html
vim _layouts/post.html
```

### Style Updates

**Edit SCSS files:**
```bash
vim _sass/jekyll-theme-minimal-modern-architecture.scss
vim _sass/fonts.scss
vim assets/css/style.scss
```

For design system details, see [Design System](.github/design-system.md).

### Configuration Changes

**Edit Jekyll config:**
```bash
vim _config.yml
```

**Note:** Restart dev server after config changes.

---

## Common Issues & Troubleshooting

### Issue: Jekyll not found

**Solution:**
```bash
gem install jekyll bundler
bundle install
```

### Issue: Permission errors

**Solution:**
```bash
# Use rbenv or rvm instead of system Ruby
# Or use sudo (not recommended)
sudo gem install jekyll bundler
```

### Issue: Port already in use

**Solution:**
```bash
# Use different port
bundle exec jekyll serve --port 4001

# Or kill process using port 4000
lsof -ti:4000 | xargs kill -9
```

### Issue: Changes not reflecting

**Solution:**
```bash
# Clear Jekyll cache
bundle exec jekyll clean
bundle exec jekyll serve
```

### Issue: Bundle install fails

**Solution:**
```bash
# Update bundler
gem install bundler
bundle update --bundler

# Or delete Gemfile.lock and reinstall
rm Gemfile.lock
bundle install
```

---

## Browser Compatibility

### Modern Browsers (Full Support)

- Chrome 88+
- Firefox 85+
- Safari 14+
- Edge 88+

### CSS Features Used

- CSS Custom Properties (CSS Variables)
- CSS Grid
- Flexbox
- Backdrop Filter
- Container Queries (progressive enhancement)

### Fallbacks

The site degrades gracefully on older browsers:
- Core content accessible
- Basic layout preserved
- Advanced features may not display

---

## Performance Tips

### Optimize Images

```bash
# Use image optimization tools
# Recommended: WebP format with fallbacks
# Compress images before adding to repo
```

### Minimize CSS/JS

Jekyll automatically minifies in production mode:
```bash
JEKYLL_ENV=production bundle exec jekyll build
```

### Enable Caching

GitHub Pages automatically enables caching.  
For custom hosting, configure cache headers.

---

## Stripe Payment Integration

### Business Information Setup

**Step 1: Log Into Stripe**
1. Go to https://dashboard.stripe.com
2. Sign in to your account

**Step 2: Navigate to Business Settings**
1. Click **Settings** (gear icon in top right)
2. Click **Business Details** in the left sidebar

**Step 3: Update Product Description**

Copy and paste this into **Product Description:**

```
Kushal Dhananjay Samant provides enterprise-grade SaaS development services and software subscriptions to businesses and individuals globally. Services include custom SaaS application development, cloud solutions, API integrations, database design, and proprietary software platform subscriptions. We serve clients across technology, e-commerce, healthcare, and professional services sectors. Customers discover us through our website (kvshvl.in), professional networks, and referrals. We charge via monthly/annual subscriptions for SaaS products and milestone-based payments for custom development projects. All services comply with international data protection standards (GDPR, CCPA) and industry security frameworks (SOC 2, ISO 27001).
```

**Step 4: Update Statement Descriptor**

Update "Statement descriptor" to: **KVSHVL SAAS**

This appears on customers' bank statements (max 22 characters).

**Alternatives:**
- `SAMANT SAAS DEV`
- `KUSHAL SAMANT`

**Step 5: Verify Policy URLs**

Ensure all URLs are correct:
- **Business website:** https://kvshvl.in
- **Terms of service:** https://kvshvl.in/termsofservice.html
- **Privacy policy:** https://kvshvl.in/privacypolicy.html
- **Cancellation & refund policy:** https://kvshvl.in/cancellationandrefundpolicy.html

**Step 6: Update Support Contact**

- **Support email:** writetokushaldsamant@gmail.com
- **Support phone:** +91 87796 32310
- **Customer support URL:** https://kvshvl.in/support.html

**Step 7: Review and Test**

1. Review all information for accuracy
2. Test appearance on payment pages
3. Check statement descriptor in test mode
4. Save all changes

---

### Stripe Best Practices

**Statement Descriptor:**
- Keep it recognizable to customers
- Use your business name or brand
- Avoid generic terms
- Test in Stripe's preview before going live

**Policy URL Requirements:**
- Stripe requires these URLs for compliance
- Ensure all policy pages are live and accessible
- Keep policies up to date
- Review annually or when services change

**Product Description Tips:**
- Be specific about what you offer
- Explain how you charge customers
- Mention compliance and security (builds trust)
- Update if your services change significantly

---

### Stripe Support Resources

**Stripe Documentation:** https://stripe.com/docs  
**Stripe Support:** https://support.stripe.com  
**Payment Testing:** Use Stripe test mode cards

**Test Card Numbers:**
- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
- Requires authentication: `4000 0025 0000 3155`

---

## GitHub Actions Workflows

### Automated RSS Feed Update

**File:** `.github/workflows/update_rss.yml`

Automatically generates RSS feed from blog posts.

### Automated Sitemap Update

**File:** `.github/workflows/update_sitemap.yml`

Automatically generates sitemap for all pages.

**Manual Trigger:**
```bash
# Push changes to trigger workflows
git push origin main
```

---

## Deployment

### GitHub Pages (Automatic)

**How it works:**
1. Push changes to `main` branch
2. GitHub Pages automatically builds site
3. Live site updates at https://kushalsamant.github.io
4. Custom domain (kvshvl.in) serves the site

**Configuration:**
- Settings → Pages → Source: main branch
- Custom domain: kvshvl.in (configured in CNAME file)

### Manual Deployment

```bash
# Build site locally
JEKYLL_ENV=production bundle exec jekyll build

# Output is in _site/
# Deploy _site/ to any web server
```

---

## Environment Variables

### For Local Development

```bash
# Set Jekyll environment
export JEKYLL_ENV=development

# Run server
bundle exec jekyll serve
```

### For Production

```bash
# Set production environment
export JEKYLL_ENV=production

# Build with production settings
bundle exec jekyll build
```

---

## Related Documentation

- **Technical Reference:** See [Technical](.github/technical.md)
- **Design System:** See [Design System](.github/design-system.md)
- **Business Information:** See [Business](.github/business.md)
- **Testing Guidelines:** See [Testing](.github/testing.md)

---

**Last Updated:** November 5, 2025  
**Status:** Complete Setup Guide

