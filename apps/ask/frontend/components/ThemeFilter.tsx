'use client';

import { Theme } from '@/lib/api';
import { Button } from '@kushalsamant/design-template';

interface ThemeFilterProps {
  themes: Theme[];
  selectedTheme: string | null;
  onThemeChange: (theme: string | null) => void;
}

export function ThemeFilter({ themes, selectedTheme, onThemeChange }: ThemeFilterProps) {
  return (
    <div style={{ marginBottom: 'var(--space-lg)' }}>
      <div style={{ 
        display: 'flex', 
        flexWrap: 'wrap', 
        gap: 'var(--space-sm)',
        alignItems: 'center'
      }}>
        <span style={{ 
          marginRight: 'var(--space-sm)', 
          fontSize: 'var(--font-size-sm)',
          fontWeight: 'var(--font-weight-medium)'
        }}>
          Filter by theme:
        </span>
        <Button
          variant={selectedTheme === null ? 'primary' : 'secondary'}
          onClick={() => onThemeChange(null)}
        >
          All
        </Button>
        {themes.map((theme) => (
          <Button
            key={theme.name}
            variant={selectedTheme === theme.name ? 'primary' : 'secondary'}
            onClick={() => onThemeChange(theme.name)}
          >
            {theme.name} ({theme.count})
          </Button>
        ))}
      </div>
    </div>
  );
}

