# KVSHVL Design System

> Unified design system for all KVSHVL products: Reframe, Ask, and Emoji Mosaic

---

## Brand Colors

### Primary Brand

```
Purple (Primary): #9333EA
Pink (Secondary): #EC4899
```

### Product-Specific Colors

**Reframe**
- Primary: #9333EA (Purple)
- Secondary: #EC4899 (Pink)
- Gradient: `from-purple-500 to-pink-500`

**Ask**
- Primary: #3B82F6 (Blue)
- Secondary: #06B6D4 (Cyan)
- Gradient: `from-blue-500 to-cyan-500`

**Emoji Mosaic**
- Primary: #F97316 (Orange)
- Secondary: #FBBF24 (Yellow)
- Gradient: `from-orange-500 to-yellow-500`

---

## Typography

### Font Family
- **Default**: Inter (Google Fonts)

### Font Sizes
- **xs**: 12px
- **sm**: 14px
- **base**: 16px
- **lg**: 18px
- **xl**: 20px
- **2xl**: 24px
- **3xl**: 30px
- **4xl**: 36px
- **5xl**: 48px

### Font Weights
- **Normal**: 400
- **Medium**: 500
- **Semibold**: 600
- **Bold**: 700

---

## Spacing System

- **xs**: 8px
- **sm**: 12px
- **md**: 16px
- **lg**: 24px
- **xl**: 32px
- **2xl**: 48px
- **3xl**: 64px

---

## Shared Components

### AppHeader

Consistent navigation header across all products.

**Parameters:**
- `product_name` (optional) - Name of the product (e.g., "Reframe", "Ask")
- `product_gradient` (optional) - Gradient classes for styling

**Usage:**
```liquid
{% comment %} Portfolio (no product name) {% endcomment %}
{% include kvshvl/app-header.html %}

{% comment %} Product page {% endcomment %}
{% include kvshvl/app-header.html product_name="Reframe" product_gradient="from-purple-500 to-pink-500" %}
```

**Features:**
- KVSHVL logo with brand gradient
- Product name separator
- Responsive design
- Sticky header

---

### AppFooter

Consistent footer with product links and branding.

**Parameters:**
- `product_links` (optional) - Array of footer links with `label`, `href`, and optional `external`
- `show_branding` (optional) - Show "Built by Kushal Samant" (default: true)

**Usage:**
```liquid
{% assign footer_links = site.data.footer_links %}
{% include kvshvl/app-footer.html product_links=footer_links show_branding=true %}
```

**Example in `_data/footer_links.yml`:**
```yaml
- label: "Pricing"
  href: "/reframe/pricing"
- label: "Terms"
  href: "/reframe/terms"
  external: false
```

---

### AppButton

Branded button component with multiple variants.

**Parameters:**
- `variant` (optional) - "primary", "secondary", "ghost", or "product" (default: "primary")
- `size` (optional) - "sm", "md", or "lg" (default: "md")
- `text` - Button text content
- `href` (optional) - Link URL (if provided, renders as `<a>`, otherwise `<button>`)
- `full_width` (optional) - "true" for full width button
- `product_color` (optional) - Custom color for product variant

**Usage:**
```liquid
{% include kvshvl/app-button.html variant="primary" size="md" text="Get Started" %}

{% include kvshvl/app-button.html variant="secondary" text="Learn More" href="/about" %}

{% include kvshvl/app-button.html variant="product" text="Launch" href="https://reframe.vercel.app" full_width="true" %}
```

**Variants:**
- **Primary**: Purple solid background, white text
- **Secondary**: Purple outline, hover fill
- **Ghost**: Transparent, hover background
- **Product**: Uses product-specific color

---

### AppCard

Content card with consistent padding and shadows.

**Parameters:**
- `variant` (optional) - "default", "product", or "flat" (default: "default")
- `padding` (optional) - "sm", "md", or "lg" (default: "md")
- `product_gradient` (optional) - Gradient classes for product variant
- `content` - The card content to display

**Usage:**
```liquid
{% capture card_content %}
  <h3>Card Title</h3>
  <p>Card content goes here</p>
{% endcapture %}
{% include kvshvl/app-card.html variant="default" padding="lg" content=card_content %}
```

---

### AppContainer

Responsive container with max-width and padding.

**Parameters:**
- `max_width` (optional) - "sm", "md", "lg", "xl", "2xl", "3xl", "7xl", or "full" (default: "7xl")
- `padding` (optional) - true/false for horizontal padding (default: true)
- `padding_y` (optional) - true/false for vertical padding (default: false)
- `center` (optional) - true/false for centering (default: true)
- `content` - The container content to display

**Usage:**
```liquid
{% capture container_content %}
  <h1>Page Content</h1>
  <p>Main content area</p>
{% endcapture %}
{% include kvshvl/app-container.html max_width="7xl" padding=true padding_y=true content=container_content %}
```

---

### ProductCard

Product showcase card for portfolio and cross-promotion.

**Parameters:**
- `name` - Product name
- `description` - Product description
- `icon` (optional) - Icon include path
- `gradient` - Gradient classes (e.g., "from-purple-500 to-pink-500")
- `status` - "live" or "soon"
- `href` - Link URL

**Usage:**
```liquid
{% include kvshvl/product-card.html 
   name="Reframe" 
   description="Professional text rewriting with 6 authentic tones and 9 generation styles." 
   gradient="from-purple-500 to-pink-500" 
   status="live" 
   href="https://reframe.vercel.app" %}
```

---

## Layout Patterns

### Full Page Layout

```liquid
<div style="min-height: 100vh; display: flex; flex-direction: column;">
  {% include kvshvl/app-header.html product_name="Product" %}
  
  <main style="flex: 1;">
    {% capture main_content %}
      <h1>Page Content</h1>
    {% endcapture %}
    {% include kvshvl/app-container.html padding_y=true content=main_content %}
  </main>
  
  {% include kvshvl/app-footer.html %}
</div>
```

### Centered Content

```liquid
<div style="min-height: 100vh; display: flex; align-items: center; justify-content: center;">
  {% capture centered_content %}
    {% capture card_content %}
      <h2>Centered Content</h2>
      <p>This content is centered on the page</p>
    {% endcapture %}
    {% include kvshvl/app-card.html padding="lg" content=card_content %}
  {% endcapture %}
  {% include kvshvl/app-container.html max_width="2xl" content=centered_content %}
</div>
```

---

## Accessibility Guidelines

### Keyboard Navigation
- All interactive elements must be keyboard accessible
- Focus states must be visible
- Skip links for main content

### Color Contrast
- Text must meet WCAG AA standards (4.5:1 for normal text)
- Interactive elements must have visible focus indicators

### Screen Readers
- Use semantic HTML (`<header>`, `<main>`, `<footer>`, `<nav>`)
- Provide `aria-label` for icon-only buttons
- Use descriptive link text (avoid "click here")

### Testing
- Test with keyboard only (no mouse)
- Test with screen reader (NVDA, VoiceOver)
- Test at 200% zoom
- Test on mobile devices

---

## Do's and Don'ts

### ✅ Do:

- Use shared components for consistency
- Follow the spacing system
- Maintain brand colors
- Test on mobile and desktop
- Keep accessibility in mind
- Use AppContainer for max-width management
- Prefer AppButton over custom buttons

### ❌ Don't:

- Create duplicate components
- Use hardcoded colors (use SCSS variables)
- Skip accessibility attributes
- Ignore responsive design
- Mix different button styles in the same context
- Create custom padding/spacing outside the system

---

## Design Tokens Reference

All design tokens are available in `_sass/design-tokens.scss`:

```scss
@import "design-tokens";

// Use in custom SCSS
.my-component {
  color: $kvshvl-primary;
  font-size: $font-size-3xl;
  padding: $spacing-lg;
  box-shadow: $shadow-lg;
}
```

SCSS variables available:
- Colors: `$kvshvl-primary`, `$reframe-primary`, `$ask-primary`, etc.
- Typography: `$font-size-*`, `$font-weight-*`, `$line-height-*`
- Spacing: `$spacing-*`
- Shadows: `$shadow-*`
- Border radius: `$border-radius-*`
- Breakpoints: `$breakpoint-*`
- Z-index: `$z-index-*`

---

## Questions or Issues?

If you encounter design inconsistencies or need clarification on component usage, refer to:
1. This documentation
2. Component source files in `_includes/kvshvl/`
3. Design tokens in `_sass/design-tokens.scss`
4. Component styles in `_sass/kvshvl-components.scss`

---

**Last Updated**: November 2025
**Maintained By**: Kushal Samant

