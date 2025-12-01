'use client';

import { useEffect, useState } from 'react';
import { getThemes, Theme } from '@/lib/ask/api';
import { GenerationForm } from '@/components/ask/GenerationForm';

export default function GeneratePage() {
  const [themes, setThemes] = useState<Theme[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadThemes() {
      try {
        const data = await getThemes();
        setThemes(data.themes);
      } catch (error) {
        console.error('Failed to load themes:', error);
      } finally {
        setLoading(false);
      }
    }
    loadThemes();
  }, []);

  return (
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article className="fade-in">
        <section className="hero" aria-labelledby="hero-title" style={{ marginBottom: 'var(--space-2xl)' }}>
          <h1 id="hero-title" className="hero-title" style={{ 
            fontSize: 'var(--font-size-4xl)', 
            marginBottom: 'var(--space-lg)',
            lineHeight: 'var(--line-height-tight)'
          }}>
            Generate New Research Content
          </h1>
          
          <p className="hero-subtitle" style={{ 
            fontSize: 'var(--font-size-xl)', 
            marginBottom: 'var(--space-md)',
            color: 'var(--color-text-secondary)'
          }}>
            Create new Q&A pairs with automated question and answer generation
          </p>
          
          <p style={{ 
            fontSize: 'var(--font-size-lg)', 
            lineHeight: 'var(--line-height-relaxed)',
            maxWidth: '65ch',
            color: 'var(--color-text-secondary)'
          }}>
            Select a research theme and generate new content. The generation process may take several minutes.
          </p>
        </section>

        <div style={{ 
          maxWidth: '600px', 
          margin: 'var(--space-2xl) auto'
        }}>
          {loading ? (
            <div style={{ textAlign: 'center', padding: 'var(--space-2xl)' }}>
              <div style={{ 
                display: 'inline-block',
                width: '40px', 
                height: '40px', 
                border: '3px solid var(--color-border)',
                borderTopColor: 'var(--color-primary)',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite'
              }} />
              <style jsx>{`
                @keyframes spin {
                  to { transform: rotate(360deg); }
                }
              `}</style>
            </div>
          ) : (
            <GenerationForm themes={themes} />
          )}
        </div>
      </article>
    </main>
  );
}

