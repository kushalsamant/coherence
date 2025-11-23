# Testing Guidelines

Comprehensive testing recommendations for the KVSHVL website to ensure quality, performance, and compatibility across all platforms.

---

## Manual Testing

### 1. Navigation Flow Testing

**Header Navigation:**
- Click through all main navigation links
- Verify correct page loads
- Check active state indicators
- Test mobile menu toggle (if applicable)

**Main Pages to Test:**
- Home → `kushalsamant.github.io/`
- About → `kushalsamant.github.io/about.html`
- People → `kushalsamant.github.io/people.html`
- Projects → `kushalsamant.github.io/projects.html`
- Get in Touch → `kushalsamant.github.io/support.html`

**Footer Links:**
- Test all 28 social media and portfolio platform links
- Verify links open in new tabs (where appropriate)
- Check legal policy links:
  - Terms of Service
  - Privacy Policy
  - Cancellation & Refund Policy
  - Support page

**Call-to-Action:**
- Test "Book a 1:1 Consultation" button
- Verify Setmore booking link works
- Check that booking page loads correctly

---

### 2. Mobile Responsiveness Testing

**Test on iPhone (Safari):**
- Portrait and landscape orientations
- Different iPhone models (SE, 12, 13, 14, etc.)
- Touch target sizes (minimum 44x44px)
- Scroll behavior
- Font readability

**Test on Android (Chrome):**
- Portrait and landscape orientations
- Different screen sizes (small, medium, large)
- Touch interactions
- Navigation menu functionality
- Form inputs (if applicable)

**Test on Tablet (iPad):**
- Portrait and landscape modes
- iPad mini, iPad Air, iPad Pro sizes
- Two-column layouts
- Touch gestures
- Keyboard interactions

**Responsive Checkpoints:**
- Verify touch targets are adequate (44x44px minimum)
- Check text is readable without zooming
- Ensure buttons are easily tappable
- Test horizontal scrolling (should be none)
- Verify images scale properly

---

### 3. Cross-Browser Testing

**Chrome (Latest Version):**
- Windows, Mac, Linux
- Rendering consistency
- JavaScript functionality
- CSS Grid and Flexbox
- Custom fonts loading

**Firefox (Latest Version):**
- Windows, Mac, Linux
- Rendering differences
- Performance
- Developer tools testing

**Safari (Latest Version):**
- Mac, iOS
- WebKit-specific features
- Touch events
- Font rendering
- Video/audio (if applicable)

**Edge (Latest Version):**
- Windows
- Chromium-based Edge
- Legacy compatibility
- Performance metrics

**Test Cases:**
- Page load times
- Interactive elements
- Form submissions (if any)
- Navigation behavior
- Typography rendering
- Color consistency
- Animation smoothness

---

### 4. Performance Testing

**PageSpeed Insights:**
- Run test: https://pagespeed.web.dev/
- Test both mobile and desktop
- Target score: 90+ for performance
- Check Core Web Vitals:
  - LCP (Largest Contentful Paint) < 2.5s
  - FID (First Input Delay) < 100ms
  - CLS (Cumulative Layout Shift) < 0.1

**Lighthouse Audit:**
- Performance: 90+
- Accessibility: 90+
- Best Practices: 90+
- SEO: 90+

**What to Check:**
- Image optimization
- CSS and JavaScript minification
- Render-blocking resources
- Browser caching
- Server response time
- Resource compression

**Core Web Vitals:**
- Largest Contentful Paint (LCP)
- First Input Delay (FID)
- Cumulative Layout Shift (CLS)
- First Contentful Paint (FCP)
- Time to Interactive (TTI)

---

## Automated Testing

### 1. W3C Validation

**HTML Validation:**
- Tool: https://validator.w3.org/
- Run on rendered pages
- Fix any errors or warnings
- Check semantic HTML structure
- Verify proper nesting

**CSS Validation:**
- Tool: https://jigsaw.w3.org/css-validator/
- Validate compiled CSS
- Check for browser compatibility
- Verify vendor prefixes
- Test custom properties

**Accessibility (WCAG 2.1):**
- Tool: https://wave.webaim.org/
- Level AA compliance minimum
- Check color contrast ratios
- Verify keyboard navigation
- Test with screen readers:
  - NVDA (Windows)
  - JAWS (Windows)
  - VoiceOver (Mac/iOS)
  - TalkBack (Android)

---

### 2. SEO Audit

**Meta Tags Verification:**
- Verify meta description on all pages
- Check meta keywords (if used)
- Validate Open Graph tags
- Check Twitter Card tags
- Verify canonical URLs

**robots.txt:**
- Location: `/robots.txt`
- Verify crawler access rules
- Check sitemap reference
- Test with Google Search Console

**sitemap.xml:**
- Location: `/marketing/sitemap/`
- Verify all 325+ pages included
- Check last modified dates
- Validate XML structure
- Submit to Google Search Console

**Mobile-Friendliness:**
- Tool: https://search.google.com/test/mobile-friendly
- Verify responsive design
- Check viewport configuration
- Test font sizes
- Verify touch elements

**Structured Data:**
- Tool: https://search.google.com/structured-data/testing-tool
- Test organization markup
- Verify breadcrumb navigation
- Check article/blog post markup

---

## Content Testing

### Link Testing

**Internal Links:**
- Check all 296 anthology post links
- Verify project page links
- Test navigation links
- Check cross-references in legal docs

**External Links:**
- Verify 28 social media links
- Test portfolio platform links
- Check Setmore booking link
- Verify legal policy URLs

**Broken Link Checker:**
- Use online tools or scripts
- Test all internal links
- Verify external links still work
- Check for 404 errors

---

### Text Content

**Spelling and Grammar:**
- Proofread all pages
- Use spell-check tools
- Verify technical terminology
- Check brand name consistency (KVSHVL)

**Contact Information:**
- Email: writetokushaldsamant@gmail.com
- Phone: +91 87796 32310
- Address consistency
- Hours of operation
- Verify all instances match

---

## Analytics Testing

### Google Analytics 4

**Setup Verification:**
- GA4 Property ID: G-0LNSC1VBGQ
- Real-time reports working
- Page view tracking
- Event tracking (if configured)
- Conversion tracking (if applicable)

**Google Tag Manager:**
- GTM Container: GTM-KXDZLM4W
- Tags firing correctly
- Triggers working
- Variables configured
- Debug mode testing

---

## Security Testing

### HTTPS Verification

- ✅ SSL certificate valid
- ✅ HTTPS redirect working
- ✅ Mixed content warnings (none)
- ✅ Secure headers configured

### Privacy & Compliance

- ✅ Cookie consent (if required)
- ✅ Privacy policy accessible
- ✅ Terms of service accessible
- ✅ Data protection measures documented

---

## Pre-Deployment Checklist

### Critical Tests

- [x] All broken links fixed (Links page created, redirects configured)
- [x] Navigation working correctly (Links page added to header navigation)
- [x] Legal documentation accessible (All legal pages verified)
- [x] Contact information correct (Verified in getintouch page)
- [ ] Analytics configured and tracking (Requires manual verification on live site)
- [x] Meta tags optimized (SEO metadata added to all pages)
- [ ] Mobile responsive (Requires manual testing)
- [ ] Cross-browser compatible (Requires manual testing)
- [ ] Performance score 90+ (Requires Lighthouse audit)
- [ ] Accessibility compliant (Requires accessibility audit)
- [x] SEO optimized (Schema.org structured data added)

### Post-Deployment Actions

- [x] DNS verification (kvshvl.in configured per README)
- [x] SSL certificate working (Vercel auto-provisions SSL)
- [ ] Analytics receiving data (Requires manual verification)
- [ ] Browser testing on live site (Requires manual testing)
- [ ] Performance check on production (Requires Lighthouse audit on live site)
- [x] Setmore integration working (Setmore link verified in getintouch page)
- [x] Social media links updated (Links page created with all 15+ social/portfolio links)
- [ ] Submit sitemap to search engines (Requires manual action)

---

## Regression Testing

### When to Test

Test after:
- Content updates
- Design changes
- New feature additions
- Jekyll version updates
- Theme modifications
- Plugin updates

### What to Test

- Core functionality
- Navigation flow
- Form submissions (if any)
- Third-party integrations
- Analytics tracking
- Mobile responsiveness
- Cross-browser compatibility

---

## Bug Reporting

### Information to Include

1. **Description:** Clear description of the issue
2. **Steps to Reproduce:** Detailed steps
3. **Expected Behavior:** What should happen
4. **Actual Behavior:** What actually happened
5. **Environment:**
   - Browser and version
   - Operating system
   - Device type
   - Screen resolution
6. **Screenshots/Videos:** Visual evidence
7. **Console Errors:** Browser console logs

### Reporting Channels

- GitHub Issues: https://github.com/kushalsamant/kushalsamant.github.io/issues
- Email: writetokushaldsamant@gmail.com

---

## Tools & Resources

### Testing Tools

- **PageSpeed Insights:** https://pagespeed.web.dev/
- **Lighthouse:** Built into Chrome DevTools
- **W3C Validator:** https://validator.w3.org/
- **WAVE:** https://wave.webaim.org/
- **Mobile-Friendly Test:** https://search.google.com/test/mobile-friendly
- **Google Search Console:** https://search.google.com/search-console

### Browser Testing

- **BrowserStack:** Cross-browser testing platform
- **LambdaTest:** Browser compatibility testing
- **Chrome DevTools:** Device emulation

---

## Related Documentation

- **Production Status:** See [Production Status](.github/production-status.md)
- **Technical Reference:** See [Technical](.github/technical.md)
- **Design System:** See [Design System](.github/design-system.md)

---

**Last Updated:** November 5, 2025  
**Status:** Production Testing Guidelines

