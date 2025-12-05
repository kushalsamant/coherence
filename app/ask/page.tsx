'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, Button } from '@kushalsamant/design-template';
import { startGeneration, GenerateStartRequest } from '@/lib/ask/api';

export default function Home() {
  const router = useRouter();
  const [keywords, setKeywords] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);

  const validateKeywords = (keywordsInput: string): [boolean, string | null] => {
    if (!keywordsInput || !keywordsInput.trim()) {
      return [false, 'Keywords cannot be empty'];
    }

    const keywordList = keywordsInput.split(',').map(kw => kw.trim()).filter(kw => kw.length > 0);

    if (keywordList.length === 0) {
      return [false, 'At least one keyword is required'];
    }

    for (const keyword of keywordList) {
      const wordCount = keyword.split(/\s+/).filter(w => w.length > 0).length;
      if (wordCount > 2) {
        return [false, `Keyword "${keyword}" has more than 2 words. Each keyword must be 1-2 words maximum.`];
      }
      if (wordCount === 0) {
        return [false, 'Empty keyword found'];
      }
    }

    return [true, null];
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setValidationError(null);

    const [isValid, errorMsg] = validateKeywords(keywords);
    if (!isValid) {
      setValidationError(errorMsg || 'Invalid keywords');
      return;
    }

    setLoading(true);
    try {
      const request: GenerateStartRequest = {
        keywords: keywords.trim(),
      };

      const response = await startGeneration(request);

      if (response.success && response.session_id) {
        // Redirect to generation flow page
        router.push(`/generate/flow?session=${response.session_id}`);
      } else {
        setError(response.error || response.message || 'Failed to start generation');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start generation');
      } finally {
        setLoading(false);
      }
  };

  return (
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto', textAlign: 'center' }}>
      <article className="fade-in">
        {/* Hero Section */}
        <section className="hero" aria-labelledby="hero-title" style={{ marginBottom: 'var(--space-2xl)' }}>
          <h1 id="hero-title" className="hero-title" style={{ 
            fontSize: 'var(--font-size-4xl)', 
            marginBottom: 'var(--space-lg)',
            lineHeight: 'var(--line-height-tight)',
            textAlign: 'center'
          }}>
            ASK: Daily Research
          </h1>
          
          <p className="hero-subtitle" style={{ 
            fontSize: 'var(--font-size-xl)', 
            marginBottom: 'var(--space-md)',
            color: 'var(--color-text-secondary)',
            textAlign: 'center'
          }}>
            Generate research Q&A pairs from keywords using AI
          </p>
          
          <p style={{ 
            fontSize: 'var(--font-size-lg)', 
            lineHeight: 'var(--line-height-relaxed)',
            maxWidth: '65ch',
            color: 'var(--color-text-secondary)',
            marginBottom: 'var(--space-xl)',
            textAlign: 'center',
            margin: '0 auto var(--space-xl)'
          }}>
            Enter keywords (1-2 words each, separated by commas) to start generating a chain of research questions and answers.
          </p>
        </section>

        {/* Keyword Input Form */}
        <section style={{ maxWidth: '600px', margin: '0 auto' }}>
          <Card variant="default">
            <form onSubmit={handleSubmit}>
              <div style={{ marginBottom: 'var(--space-lg)' }}>
                <label htmlFor="keywords" style={{ 
                  display: 'block', 
                  marginBottom: 'var(--space-sm)',
                  fontSize: 'var(--font-size-base)',
                  fontWeight: 'var(--font-weight-medium)'
                }}>
                  Enter Keywords
                </label>
                <input
                  id="keywords"
                  type="text"
                  value={keywords}
                  onChange={(e) => {
                    setKeywords(e.target.value);
                    setValidationError(null);
                    setError(null);
                  }}
                  placeholder="e.g., quantum physics, machine learning, sustainable design"
                  disabled={loading}
                  style={{
                    width: '100%',
                    padding: 'var(--space-md)',
                    borderRadius: 'var(--radius-md)',
                    border: validationError || error ? '2px solid var(--color-error, #c00)' : '1px solid var(--color-border)',
                    backgroundColor: 'var(--color-background)',
                    color: 'var(--color-text)',
                    fontSize: 'var(--font-size-base)'
                  }}
                />
                <p style={{ 
                  marginTop: 'var(--space-xs)',
                  fontSize: 'var(--font-size-sm)',
                  color: 'var(--color-text-secondary)'
                }}>
                  Each keyword should be 1-2 words maximum. Separate multiple keywords with commas.
                </p>
              </div>

              {validationError && (
                <div style={{ 
                  marginBottom: 'var(--space-md)', 
                  padding: 'var(--space-sm) var(--space-md)',
                  backgroundColor: 'var(--color-error-bg, #fee)',
                  color: 'var(--color-error, #c00)',
                  borderRadius: 'var(--radius-md)',
                  fontSize: 'var(--font-size-sm)'
                }}>
                  {validationError}
              </div>
              )}

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

              <div style={{ width: '100%', display: 'flex', justifyContent: 'center' }}>
                <Button
                  type="submit"
                  variant="primary"
                  disabled={loading || !keywords.trim()}
                >
                  {loading ? 'Starting...' : 'Start Generation'}
                </Button>
              </div>
            </form>
            </Card>

          {/* Quick Links */}
          <div style={{ 
            marginTop: 'var(--space-xl)',
            textAlign: 'center'
          }}>
            <a href="/ask/browse" style={{ 
              textDecoration: 'none',
              color: 'var(--color-text-secondary)',
              fontSize: 'var(--font-size-sm)'
            }}>
              Browse existing Q&A pairs →
            </a>
          </div>
        </section>
      </article>
    </main>
  );
}
