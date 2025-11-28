'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { getQAPair, QAPair } from '@/lib/api';
import { Button, Card } from '@kushalsamant/design-template';

export default function QADetailPage() {
  const params = useParams();
  const router = useRouter();
  const questionNumber = parseInt(params.id as string);
  
  const [qaPair, setQAPair] = useState<QAPair | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadQAPair() {
      try {
        setLoading(true);
        const data = await getQAPair(questionNumber);
        setQAPair(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load Q&A pair');
      } finally {
        setLoading(false);
      }
    }
    loadQAPair();
  }, [questionNumber]);

  if (loading) {
    return (
      <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
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
      </main>
    );
  }

  if (error || !qaPair) {
    return (
      <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
        <Card variant="default">
          <p style={{ color: 'var(--color-error, #c00)' }}>{error || 'Q&A pair not found'}</p>
          <a href="/browse" style={{ textDecoration: 'none', display: 'inline-block', marginTop: 'var(--space-md)' }}>
            <Button variant="secondary">Back to Browse</Button>
          </a>
        </Card>
      </main>
    );
  }

  const allAnswerImages = qaPair.answer_image_urls.length > 0 
    ? qaPair.answer_image_urls 
    : qaPair.answer_image_url 
      ? [qaPair.answer_image_url] 
      : [];

  return (
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article className="fade-in">
        {/* Navigation */}
        <div style={{ marginBottom: 'var(--space-lg)' }}>
          <a href="/browse" style={{ textDecoration: 'none', display: 'inline-block' }}>
            <Button variant="secondary">← Back to Browse</Button>
          </a>
        </div>

        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
          gap: 'var(--space-xl)',
          marginBottom: 'var(--space-xl)'
        }}>
          {/* Question Section */}
          <Card variant="default">
            <div style={{ 
              display: 'inline-block', 
              padding: 'var(--space-xs) var(--space-sm)', 
              backgroundColor: 'var(--color-surface)', 
              borderRadius: 'var(--radius-sm)',
              fontSize: 'var(--font-size-xs)',
              marginBottom: 'var(--space-md)'
            }}>
              {qaPair.theme} • ASK-{qaPair.question_number.toString().padStart(3, '0')}
            </div>

            <h2 style={{ 
              marginBottom: 'var(--space-md)', 
              fontSize: 'var(--font-size-2xl)',
              lineHeight: '1.4'
            }}>
              {qaPair.question}
            </h2>
          </Card>

          {/* Answer Section */}
          <Card variant="default">
            <h3 style={{ 
              marginBottom: 'var(--space-md)', 
              fontSize: 'var(--font-size-xl)'
            }}>
              Answer
            </h3>

            <p style={{ 
              lineHeight: '1.8',
              fontSize: 'var(--font-size-base)',
              whiteSpace: 'pre-wrap'
            }}>
              {qaPair.answer}
            </p>
          </Card>
        </div>

        {/* Navigation to Previous/Next */}
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between',
          gap: 'var(--space-md)'
        }}>
          <Button
            variant="secondary"
            onClick={() => router.push(`/qa/${Math.max(1, questionNumber - 1)}`)}
            disabled={questionNumber <= 1}
          >
            ← Previous
          </Button>
          <Button
            variant="secondary"
            onClick={() => router.push(`/qa/${questionNumber + 1}`)}
          >
            Next →
          </Button>
        </div>
      </article>
    </main>
  );
}

