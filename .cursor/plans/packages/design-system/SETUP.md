# Setup Guide

Quick setup guide for the KVSHVL Design Template repository.

## Initial Setup

The design system is part of the `kushalsamant.github.io` monorepo. To work with it:

1. **Clone the Monorepo**

```bash
git clone https://github.com/kushalsamant/kushalsamant.github.io.git
cd kushalsamant.github.io/packages/design-system
```

2. **Install Dependencies**

```bash
npm install
```

4. **Build the Package**

```bash
npm run build
```

## Publishing to npm

1. **Login to npm**

```bash
npm login
```

2. **Publish Package**

```bash
npm publish --access public
```

For private packages:
```bash
npm publish --access restricted
```

3. **Version Updates**

```bash
npm version patch  # 1.0.0 -> 1.0.1
npm version minor  # 1.0.0 -> 1.1.0
npm version major  # 1.0.0 -> 2.0.0
npm publish
```

## Using in Projects

### Install

```bash
npm install @kvshvl/design-template
```

### Import

```typescript
import { AppHeader, AppFooter, Hero, Button } from '@kvshvl/design-template'
import '@kvshvl/design-template/styles/globals.css'
```

## Automatic Updates Setup

### Dependabot Configuration

Create `.github/dependabot.yml` in each project:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

### GitHub Actions (Optional)

Create `.github/workflows/update-template.yml` in template repo:

```yaml
name: Auto Publish
on:
  push:
    branches: [main]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run build
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{secrets.NPM_TOKEN}}
```

## Next Steps

- Review [README.md](./README.md) for usage
- Check [Component Documentation](./docs/COMPONENTS.md)
- See [Migration Guide](./docs/MIGRATION.md) for existing projects

