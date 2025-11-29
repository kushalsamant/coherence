# Design System Documentation

Complete guide to the KVSHVL Design System tokens, patterns, and best practices.

## Color System

### Brand Colors

- **Primary**: `#9333EA` (Purple)
- **Secondary**: `#EC4899` (Pink)
- **Gradient**: Primary to Secondary

Override in your CSS:
```css
:root {
  --color-kvshvl-primary: #your-color;
  --color-kvshvl-secondary: #your-color;
}
```

### Theme Colors

**Light Theme:**
- Background: `#ffffff`
- Background Secondary: `#f9fafb`
- Text: `#1f2937`
- Text Secondary: `#6b7280`
- Text Muted: `#9ca3af`

**Dark Theme:**
- Background: `#0a0a0a`
- Background Secondary: `#111111`
- Text: `#f9fafb`
- Text Secondary: `#d1d5db`
- Text Muted: `#9ca3af`

## Typography

### Font Family

- **Primary**: Inter (Google Fonts)
- **Monospace**: Courier New, Courier, monospace

### Font Sizes

- `--font-size-xs`: 0.75rem (12px)
- `--font-size-sm`: 0.875rem (14px)
- `--font-size-base`: 1rem (16px)
- `--font-size-lg`: 1.125rem (18px)
- `--font-size-xl`: 1.25rem (20px)
- `--font-size-2xl`: 1.5rem (24px)
- `--font-size-3xl`: 1.875rem (30px)
- `--font-size-4xl`: 2.25rem (36px)
- `--font-size-5xl`: 3rem (48px)

### Font Weights

- Normal: 400
- Medium: 500
- Semibold: 600
- Bold: 700

### Line Heights

- Tight: 1.25
- Normal: 1.5
- Relaxed: 1.75

## Spacing

- `--space-xs`: 0.5rem (8px)
- `--space-sm`: 0.75rem (12px)
- `--space-md`: 1rem (16px)
- `--space-lg`: 1.5rem (24px)
- `--space-xl`: 2rem (32px)
- `--space-2xl`: 3rem (48px)
- `--space-3xl`: 4rem (64px)

## Border Radius

- `--radius-sm`: 0.375rem (6px)
- `--radius-md`: 0.5rem (8px)
- `--radius-lg`: 0.75rem (12px)
- `--radius-xl`: 1rem (16px)
- `--radius-2xl`: 1.5rem (24px)
- `--radius-full`: 9999px

## Shadows

- `--shadow-sm`: Subtle shadow
- `--shadow-base`: Base shadow
- `--shadow-md`: Medium shadow
- `--shadow-lg`: Large shadow

## Transitions

- `--transition-fast`: 150ms
- `--transition-base`: 300ms
- `--transition-slow`: 500ms

## Layout

- `--container-max-width`: 80rem (1280px)
- `--container-width`: 90%

## Z-Index

- Sticky: 20
- Fixed: 30
- Dropdown: 40
- Modal: 50

## Utility Classes

### Gradient Text

```html
<h1 className="gradient-text">Gradient Text</h1>
```

### Scroll Animations

```html
<div className="scroll-fade-in">Content</div>
```

### Fade In

```html
<div className="fade-in">Content</div>
```

### Slide Up

```html
<div className="slide-up">Content</div>
```

## Grid Layouts

```html
<div className="grid grid-2">
  <!-- 2 columns -->
</div>

<div className="grid grid-3">
  <!-- 3 columns -->
</div>
```

## Best Practices

1. **Use CSS Variables**: Always use design tokens instead of hardcoded values
2. **Responsive Design**: Use mobile-first approach
3. **Accessibility**: Maintain WCAG AAA contrast ratios
4. **Performance**: Use `will-change` sparingly, prefer transform/opacity for animations
5. **Dark Mode**: Test both light and dark themes

## Customization

### Override Colors

```css
:root {
  --color-kvshvl-primary: #your-color;
  --color-kvshvl-secondary: #your-color;
}
```

### Override Spacing

```css
:root {
  --space-xl: 3rem; /* Custom spacing */
}
```

### Custom Theme

```css
[data-theme="custom"] {
  --color-background: #custom-color;
  /* ... other overrides */
}
```

