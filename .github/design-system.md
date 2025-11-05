# Design System

A dark minimalist design system for the KVSHVL portfolio website, featuring elegant serif typography, generous whitespace, and a sophisticated monochromatic color scheme.

---

## Design Philosophy

### Dark Minimalist Approach

The design system embodies:
- **Pure Black Background**: Creates dramatic contrast and focus
- **Elegant Serif Typography**: Times-based fonts with tight kerning for sophistication
- **Generous Whitespace**: Ample spacing between elements for clarity
- **Subtle Interactions**: Minimal hover effects with underlines
- **Monochromatic Palette**: Strictly black, white, and grey tones
- **Image-Driven**: Hero carousel showcasing visual work

---

## Color Palette

### Monochromatic System

- **Pure Black**: `#000000` - Background color
- **Pure White**: `#ffffff` - Primary text color
- **Light Grey**: `#cccccc` - Secondary text color
- **Border Color**: `rgba(255, 255, 255, 0.2)` - Subtle separators

### Usage Guidelines

- **Background**: Always pure black (#000000)
- **Text**: Always white (#ffffff) or light grey (#cccccc)
- **Borders**: Always thin (1px) with subtle white opacity
- **No Colors**: Strictly monochromatic - no blues, reds, or other hues
- **Logo Images**: Inverted to white using CSS filter

---

## Typography

### Font Families

```scss
--font-family-serif: 'Times New Roman', Times, serif;
--font-family-mono: 'Courier New', Courier, monospace;
```

### Font Sizes

```scss
--font-size-sm: 0.875rem;     /* 14px */
--font-size-base: 1.625rem;   /* 26px - large body text */
--font-size-lg: 1.875rem;     /* 30px */
--font-size-xl: 2.5rem;       /* 40px */
--font-size-2xl: 3.125rem;    /* 50px */
--font-size-3xl: 3.75rem;     /* 60px */
--font-size-4xl: 4.375rem;    /* 70px - hero text */
```

### Line Heights

```scss
--line-height-tight: 1.1;     /* Headings */
--line-height-normal: 1.4;    /* Body text */
--line-height-relaxed: 1.5;   /* Long-form content */
```

### Letter Spacing

```scss
--letter-spacing-tight: -0.05em;   /* Headings - tight kerning */
--letter-spacing-normal: -0.02em;  /* Body - subtle tightness */
```

### Typography Usage

- **Headings**: Bold serif, tight line-height, negative letter-spacing
- **Body Text**: 26px base size, normal weight, subtle negative spacing
- **Links**: White text, underline on hover only
- **Emphasis**: Bold weight, same serif family

### Font Smoothing

```scss
-webkit-font-smoothing: antialiased;
-moz-osx-font-smoothing: grayscale;
```

---

## Spacing System

### Scale

```scss
--space-2: 0.5rem;    /* 8px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-24: 6rem;     /* 96px */
--space-32: 8rem;     /* 128px */
```

### Application

- **Paragraphs**: `--space-12` (48px) bottom margin
- **Sections**: `--space-16` (64px) padding
- **Hero**: `--space-32` (128px) top/bottom padding
- **Footer Columns**: `--space-16` (64px) gap

---

## Layout Components

### Hero Quote Section

- Centered text alignment
- Large serif typography (60-70px)
- Generous padding (128px top/bottom)
- Full-width black background
- Tight letter-spacing for elegance

### Image Carousel

- **Library**: Swiper.js 11.x
- **Effect**: Fade transitions
- **Auto-advance**: 5 seconds per slide
- **Navigation**: Arrow buttons, keyboard support
- **Counter**: Current/total format (1/9)
- **Controls**: White color, minimal design

### Header

- **Position**: Sticky (fixed at top)
- **Content**: Site name only (KVSHVL)
- **Border**: Thin white bottom border
- **Padding**: Minimal (32px)
- **Background**: Black with z-index 100

### Footer

- **Layout**: 3-column grid (stacks on mobile)
- **Columns**:
  1. Contact information
  2. Social links with logo images
  3. Platforms + legal links
- **Logo Images**: Inverted to white (filter: invert(1))
- **Typography**: Small text (14px)
- **Spacing**: 64px column gap

### Content Sections

- **Wrapper**: Semantic `<section>` tags
- **Grid Item**: Consistent padding
- **Multi-column**: 2 columns for lists (People page)
- **Break Inside**: Avoid for clean column breaks

---

## Interactive Elements

### Links

```scss
a {
  color: white;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 150ms;
}

a:hover {
  border-bottom-color: white;
}
```

### Buttons (Carousel Controls)

- White color
- 44px minimum touch target
- Simple chevron icons
- Hover: No color change, position shift

### Focus States

- 2px white outline
- 2px offset
- Keyboard navigation fully supported

---

## Responsive Breakpoints

### Mobile (<640px)

- Base font: 18px
- Hero text: 36-40px
- Single column footer
- Stacked navigation menu
- Full-width carousel

### Tablet (641-768px)

- Base font: 22px
- 2-column footer
- Adjusted spacing

### Desktop (1024px+)

- Base font: 26px
- 3-column footer
- Maximum spacing
- Full layout width

---

## Accessibility Features

- **Skip to Content**: Hidden link, appears on focus
- **ARIA Labels**: Carousel has proper labeling
- **Keyboard Navigation**: Full support for arrow keys
- **Focus Indicators**: White outline on all interactive elements
- **Contrast Ratio**: Excellent (white on black)
- **Font Smoothing**: Antialiased for clarity

---

## Custom Features

### Scrollbar Styling

```scss
::-webkit-scrollbar {
  width: 12px;
  background: black;
}

::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
}
```

### Multi-Column Layout

```scss
.content-columns {
  column-count: 2;
  column-gap: 64px;
  column-rule: 1px solid rgba(255, 255, 255, 0.2);
}
```

Used on People page for elegant name listing.

---

## File Structure

### Main Stylesheet

- `_sass/portfolio-dark-theme.scss` - Complete design system
- `assets/css/style.scss` - Import file
- `assets/js/slideshow.js` - Swiper configuration

### Assets

- `/assets/img/` - Images and logos
- `/assets/img/favicon.svg` - Black/white SVG favicon
- `/assets/fonts/` - Font files (Noto Sans legacy)

---

## Design Principles

1. **Monochromatic**: Only black, white, grey
2. **Serif Typography**: Elegant, traditional fonts
3. **Negative Space**: Generous whitespace throughout
4. **Minimal Borders**: Thin, subtle separators only
5. **Image Focus**: Large carousel draws attention
6. **Consistent Rhythm**: 8px base spacing grid
7. **Accessibility First**: WCAG AAA compliant
8. **Performance**: Optimized loading and rendering

---

## Component Examples

### Hero Quote

```html
<div class="hero-quote">
    <p>Action Expresses Priorities - Mahatma Gandhi</p>
</div>
```

### Slideshow Section

```html
<div class="slideshow-section">
    <div class="slideshow-container">
        <div class="swiper">...</div>
    </div>
    <div class="slideshow-info">
        <h2>KVSHVL</h2>
        <nav class="slideshow-menu">...</nav>
        <div class="slideshow-counter">1/9</div>
    </div>
</div>
```

### Footer

```html
<footer>
    <div class="footer-columns">
        <div class="footer-column">...</div>
    </div>
</footer>
```

---

**Design System Version:** 2.0 (November 5, 2025)  
**Theme Name:** Dark Minimalist Portfolio  
**Primary Typeface:** Times New Roman Serif
