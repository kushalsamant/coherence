'use client';

import { useEffect, useState } from 'react';
import { getQAPairs, getThemes, QAPair, Theme } from '@/lib/ask/api';
import { QAItem } from '@/components/ask/QAItem';
import { ThemeFilter } from '@/components/ask/ThemeFilter';
import { Button } from '@kushalsamant/design-template';

export default function BrowsePage() {
  const [qaPairs, setQAPairs] = useState<QAPair[]>([]);
  const [themes, setThemes] = useState<Theme[]>([]);
  const [selectedTheme, setSelectedTheme] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const [qaData, themesData] = await Promise.all([
          getQAPairs(selectedTheme || undefined, page, 20),
          getThemes(),
        ]);
        setQAPairs(qaData.items);
        setTotalPages(qaData.total_pages);
        setThemes(themesData.themes);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load data');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [selectedTheme, page]);

  // Filter by search query
  const filteredPairs = searchQuery
    ? qaPairs.filter(
        (qa) =>
          qa.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
          qa.answer.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : qaPairs;

  return (
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article className="fade-in">
        <h1 style={{ marginBottom: 'var(--space-lg)', fontSize: 'var(--font-size-3xl)' }}>
          Browse Research Q&A Pairs
        </h1>

        {/* Search */}
        <div style={{ marginBottom: 'var(--space-lg)' }}>
          <input
            type="text"
            placeholder="Search questions and answers..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{
              width: '100%',
              maxWidth: '500px',
              padding: 'var(--space-sm) var(--space-md)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--color-border)',
              backgroundColor: 'var(--color-background)',
              color: 'var(--color-text)',
              fontSize: 'var(--font-size-base)'
            }}
          />
        </div>

        {/* Theme Filter */}
        {themes.length > 0 && (
          <ThemeFilter
            themes={themes}
            selectedTheme={selectedTheme}
            onThemeChange={(theme) => {
              setSelectedTheme(theme);
              setPage(1);
            }}
          />
        )}

        {/* Error State */}
        {error && (
          <div style={{ 
            padding: 'var(--space-md)', 
            backgroundColor: 'var(--color-error-bg, #fee)',
            color: 'var(--color-error, #c00)',
            borderRadius: 'var(--radius-md)',
            marginBottom: 'var(--space-lg)'
          }}>
            {error}
          </div>
        )}

        {/* Loading State */}
        {loading && (
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
        )}

        {/* Q&A Pairs Grid */}
        {!loading && !error && (
          <>
            {filteredPairs.length === 0 ? (
              <div style={{ 
                textAlign: 'center', 
                padding: 'var(--space-2xl)',
                color: 'var(--color-text-secondary)'
              }}>
                <p>No Q&A pairs found.</p>
                {searchQuery && <p>Try a different search query.</p>}
              </div>
            ) : (
              <>
                <div style={{ 
                  display: 'grid', 
                  gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', 
                  gap: 'var(--space-lg)',
                  marginBottom: 'var(--space-xl)'
                }}>
                  {filteredPairs.map((qaPair) => (
                    <QAItem key={qaPair.id} qaPair={qaPair} />
                  ))}
                </div>

                {/* Pagination */}
                {!searchQuery && totalPages > 1 && (
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'center', 
                    gap: 'var(--space-sm)',
                    alignItems: 'center'
                  }}>
                    <Button
                      variant="secondary"
                      onClick={() => setPage((p) => Math.max(1, p - 1))}
                      disabled={page === 1}
                    >
                      Previous
                    </Button>
                    <span style={{ 
                      padding: 'var(--space-sm) var(--space-md)',
                      fontSize: 'var(--font-size-sm)'
                    }}>
                      Page {page} of {totalPages}
                    </span>
                    <Button
                      variant="secondary"
                      onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                      disabled={page === totalPages}
                    >
                      Next
                    </Button>
                  </div>
                )}
              </>
            )}
          </>
        )}
      </article>
    </main>
  );
}

