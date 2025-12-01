'use client';

import { useState } from 'react';
import { Button, Card } from '@kushalsamant/design-template';
import { Theme, generateContent, GenerateRequest } from '@/lib/api';
import { useRouter } from 'next/navigation';

interface GenerationFormProps {
  themes: Theme[];
}

export function GenerationForm({ themes }: GenerationFormProps) {
  const [selectedTheme, setSelectedTheme] = useState<string>('');
  const [customTheme, setCustomTheme] = useState<string>('');
  const [useCustomTheme, setUseCustomTheme] = useState<boolean>(false);
  const [count, setCount] = useState<number>(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const themeToUse = useCustomTheme ? customTheme.trim() : (selectedTheme || undefined);
      const request: GenerateRequest = {
        theme: themeToUse || undefined,
        count,
      };

      const response = await generateContent(request);

      if (response.success) {
        setSuccess(true);
        // Redirect to the first generated Q&A pair after a short delay
        if (response.qa_pairs && response.qa_pairs.length > 0) {
          setTimeout(() => {
            router.push(`/qa/${response.qa_pairs![0].question_number}`);
          }, 2000);
        } else {
          // If no Q&A pairs returned, redirect to browse page
          setTimeout(() => {
            router.push('/browse');
          }, 2000);
        }
      } else {
        setError(response.error || response.message);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate content');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card variant="default">
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 'var(--space-lg)' }}>
          <label style={{ 
            display: 'block', 
            marginBottom: 'var(--space-sm)',
            fontSize: 'var(--font-size-sm)',
            fontWeight: 'var(--font-weight-medium)'
          }}>
            Theme (Optional - Leave empty for random theme)
          </label>
          
          <div style={{ marginBottom: 'var(--space-sm)' }}>
            <label style={{ 
              display: 'flex', 
              alignItems: 'center',
              gap: 'var(--space-sm)',
              fontSize: 'var(--font-size-sm)',
              cursor: 'pointer'
            }}>
              <input
                type="radio"
                checked={!useCustomTheme}
                onChange={() => {
                  setUseCustomTheme(false);
                  setCustomTheme('');
                }}
              />
              Select from existing themes
            </label>
            <label style={{ 
              display: 'flex', 
              alignItems: 'center',
              gap: 'var(--space-sm)',
              fontSize: 'var(--font-size-sm)',
              cursor: 'pointer',
              marginTop: 'var(--space-xs)'
            }}>
              <input
                type="radio"
                checked={useCustomTheme}
                onChange={() => {
                  setUseCustomTheme(true);
                  setSelectedTheme('');
                }}
              />
              Enter custom theme
            </label>
          </div>

          {!useCustomTheme ? (
            <select
              id="theme"
              value={selectedTheme}
              onChange={(e) => setSelectedTheme(e.target.value)}
              style={{
                width: '100%',
                padding: 'var(--space-sm) var(--space-md)',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--color-border)',
                backgroundColor: 'var(--color-background)',
                color: 'var(--color-text)',
                fontSize: 'var(--font-size-base)'
              }}
            >
              <option value="">Random Theme</option>
              {themes.map((theme) => (
                <option key={theme.name} value={theme.name}>
                  {theme.name} ({theme.count} pairs)
                </option>
              ))}
            </select>
          ) : (
            <input
              type="text"
              id="customTheme"
              value={customTheme}
              onChange={(e) => setCustomTheme(e.target.value)}
              placeholder="Enter any research theme (e.g., quantum physics, marine biology, etc.)"
              style={{
                width: '100%',
                padding: 'var(--space-sm) var(--space-md)',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--color-border)',
                backgroundColor: 'var(--color-background)',
                color: 'var(--color-text)',
                fontSize: 'var(--font-size-base)'
              }}
            />
          )}
        </div>

        <div style={{ marginBottom: 'var(--space-lg)' }}>
          <label htmlFor="count" style={{ 
            display: 'block', 
            marginBottom: 'var(--space-sm)',
            fontSize: 'var(--font-size-sm)',
            fontWeight: 'var(--font-weight-medium)'
          }}>
            Number of Q&A Pairs
          </label>
          <input
            id="count"
            type="number"
            min="1"
            max="10"
            value={count}
            onChange={(e) => setCount(parseInt(e.target.value) || 1)}
            style={{
              width: '100%',
              padding: 'var(--space-sm) var(--space-md)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--color-border)',
              backgroundColor: 'var(--color-background)',
              color: 'var(--color-text)',
              fontSize: 'var(--font-size-base)'
            }}
          />
        </div>

        {error && (
          <div style={{ 
            marginBottom: 'var(--space-md)', 
            padding: 'var(--space-sm) var(--space-md)',
            backgroundColor: 'var(--color-error-bg, #fee)',
            color: 'var(--color-error, #c00)',
            borderRadius: 'var(--radius-md)',
            fontSize: 'var(--font-size-sm)'
          }}>
            {error}
          </div>
        )}

        {success && (
          <div style={{ 
            marginBottom: 'var(--space-md)', 
            padding: 'var(--space-sm) var(--space-md)',
            backgroundColor: 'var(--color-success-bg, #efe)',
            color: 'var(--color-success, #0c0)',
            borderRadius: 'var(--radius-md)',
            fontSize: 'var(--font-size-sm)'
          }}>
            Content generated successfully! Redirecting...
          </div>
        )}

        <div style={{ width: '100%' }}>
          <Button
            type="submit"
            variant="primary"
            disabled={loading}
          >
            {loading ? 'Generating...' : 'Generate Content'}
          </Button>
        </div>

        <p style={{ 
          marginTop: 'var(--space-md)', 
          fontSize: 'var(--font-size-xs)', 
          color: 'var(--color-text-secondary)',
          textAlign: 'center'
        }}>
          Generation may take several minutes. Please be patient.
        </p>
      </form>
    </Card>
  );
}

