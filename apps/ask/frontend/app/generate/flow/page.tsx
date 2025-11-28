'use client';

import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { Card, Button } from '@kushalsamant/design-template';
import { 
  generateNext, 
  updateKeywords, 
  GenerateNextRequest,
  UpdateKeywordsRequest,
  GenerationState 
} from '@/lib/api';

export default function GenerationFlowPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const sessionId = searchParams.get('session');
  
  const [keywords, setKeywords] = useState('');
  const [editingKeywords, setEditingKeywords] = useState(false);
  const [state, setState] = useState<GenerationState | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);

  useEffect(() => {
    if (!sessionId) {
      router.push('/');
      return;
    }
    // Initial state will be set after first generation
  }, [sessionId, router]);

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

  const handleUpdateKeywords = async () => {
    if (!sessionId) return;

    setValidationError(null);
    setError(null);

    const [isValid, errorMsg] = validateKeywords(keywords);
    if (!isValid) {
      setValidationError(errorMsg || 'Invalid keywords');
      return;
    }

    setLoading(true);
    try {
      const request: UpdateKeywordsRequest = {
        session_id: sessionId,
        keywords: keywords.trim(),
      };

      const response = await updateKeywords(request);

      if (response.success && response.state) {
        setState(response.state);
        setEditingKeywords(false);
        setError(null);
      } else {
        setError(response.error || response.message || 'Failed to update keywords');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update keywords');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateNext = async () => {
    if (!sessionId) return;

    setError(null);
    setLoading(true);

    try {
      const request: GenerateNextRequest = {
        session_id: sessionId,
        // Include keywords if they were edited
        keywords: editingKeywords && keywords.trim() ? keywords.trim() : undefined,
      };

      const response = await generateNext(request);

      if (response.success && response.state) {
        setState(response.state);
        setEditingKeywords(false);
        // Clear keywords input if we're not editing
        if (!editingKeywords) {
          setKeywords('');
        }
      } else {
        setError(response.error || response.message || 'Failed to generate next');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate next');
    } finally {
      setLoading(false);
    }
  };

  // Update keywords when state changes
  useEffect(() => {
    if (state && !editingKeywords) {
      setKeywords(state.keywords);
    }
  }, [state, editingKeywords]);

  if (!sessionId) {
    return null;
  }

  return (
    <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <article className="fade-in">
        {/* Header */}
        <div style={{ marginBottom: 'var(--space-xl)' }}>
          <a href="/" style={{ textDecoration: 'none', display: 'inline-block', marginBottom: 'var(--space-md)' }}>
            <Button variant="secondary">← Back to Home</Button>
          </a>
          <h1 style={{ 
            fontSize: 'var(--font-size-3xl)', 
            marginBottom: 'var(--space-md)'
          }}>
            Generation Flow
          </h1>
        </div>

        {/* Keywords Section - Always Editable */}
        <Card variant="default" style={{ marginBottom: 'var(--space-xl)' }}>
          <div style={{ marginBottom: 'var(--space-md)' }}>
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: 'var(--space-sm)'
            }}>
              <label htmlFor="keywords-edit" style={{ 
                fontSize: 'var(--font-size-base)',
                fontWeight: 'var(--font-weight-medium)'
              }}>
                Keywords
              </label>
              {!editingKeywords && (
                <Button
                  variant="secondary"
                  onClick={() => setEditingKeywords(true)}
                  style={{ fontSize: 'var(--font-size-sm)' }}
                >
                  Edit Keywords
                </Button>
              )}
            </div>

            {editingKeywords ? (
              <div>
                <input
                  id="keywords-edit"
                  type="text"
                  value={keywords}
                  onChange={(e) => {
                    setKeywords(e.target.value);
                    setValidationError(null);
                  }}
                  placeholder="e.g., quantum physics, machine learning"
                  disabled={loading}
                  style={{
                    width: '100%',
                    padding: 'var(--space-sm) var(--space-md)',
                    borderRadius: 'var(--radius-md)',
                    border: validationError ? '2px solid var(--color-error, #c00)' : '1px solid var(--color-border)',
                    backgroundColor: 'var(--color-background)',
                    color: 'var(--color-text)',
                    fontSize: 'var(--font-size-base)',
                    marginBottom: 'var(--space-sm)'
                  }}
                />
                {validationError && (
                  <p style={{ 
                    color: 'var(--color-error, #c00)',
                    fontSize: 'var(--font-size-sm)',
                    marginBottom: 'var(--space-sm)'
                  }}>
                    {validationError}
                  </p>
                )}
                <div style={{ display: 'flex', gap: 'var(--space-sm)' }}>
                  <Button
                    variant="primary"
                    onClick={handleUpdateKeywords}
                    disabled={loading}
                  >
                    Save Keywords
                  </Button>
                  <Button
                    variant="secondary"
                    onClick={() => {
                      setEditingKeywords(false);
                      setValidationError(null);
                      if (state) {
                        setKeywords(state.keywords);
                      }
                    }}
                    disabled={loading}
                  >
                    Cancel
                  </Button>
                </div>
              </div>
            ) : (
              <div style={{ 
                padding: 'var(--space-md)',
                backgroundColor: 'var(--color-surface)',
                borderRadius: 'var(--radius-md)',
                fontSize: 'var(--font-size-base)'
              }}>
                {state?.keywords || 'No keywords set'}
              </div>
            )}
          </div>
        </Card>

        {/* Error Display */}
        {error && (
          <Card variant="default" style={{ 
            marginBottom: 'var(--space-lg)',
            backgroundColor: 'var(--color-error-bg, #fee)',
            border: '1px solid var(--color-error, #c00)'
          }}>
            <p style={{ color: 'var(--color-error, #c00)' }}>{error}</p>
          </Card>
        )}

        {/* Generation Chain Display */}
        <div style={{ marginBottom: 'var(--space-xl)' }}>
          <h2 style={{ 
            fontSize: 'var(--font-size-2xl)',
            marginBottom: 'var(--space-lg)'
          }}>
            Generation Chain
          </h2>

          {state && state.qa_chain.length === 0 && !state.last_question && (
            <Card variant="default">
              <p style={{ color: 'var(--color-text-secondary)', textAlign: 'center', padding: 'var(--space-xl)' }}>
                No Q&A pairs generated yet. Click "Generate Next" to start.
              </p>
            </Card>
          )}

          {/* Display Q&A Chain */}
          {state && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
              {/* Show existing chain */}
              {state.qa_chain.map((qa, index) => (
                <div key={index} style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
                  <Card variant="default">
                    <div style={{ 
                      display: 'inline-block',
                      padding: 'var(--space-xs) var(--space-sm)',
                      backgroundColor: 'var(--color-surface)',
                      borderRadius: 'var(--radius-sm)',
                      fontSize: 'var(--font-size-xs)',
                      marginBottom: 'var(--space-sm)'
                    }}>
                      Q&A Pair {index + 1}
                    </div>
                    <h3 style={{ 
                      fontSize: 'var(--font-size-lg)',
                      marginBottom: 'var(--space-sm)',
                      color: 'var(--color-primary)'
                    }}>
                      Question {index + 1}
                    </h3>
                    <p style={{ 
                      lineHeight: '1.6',
                      marginBottom: 'var(--space-md)'
                    }}>
                      {qa.question}
                    </p>
                    <h4 style={{ 
                      fontSize: 'var(--font-size-base)',
                      marginBottom: 'var(--space-sm)',
                      color: 'var(--color-text-secondary)'
                    }}>
                      Answer {index + 1}
                    </h4>
                    <p style={{ 
                      lineHeight: '1.8',
                      whiteSpace: 'pre-wrap'
                    }}>
                      {qa.answer}
                    </p>
                  </Card>
                </div>
              ))}

              {/* Show current question if exists but no answer yet */}
              {state.last_question && !state.last_answer && (
                <Card variant="default" style={{ border: '2px solid var(--color-primary)' }}>
                  <div style={{ 
                    display: 'inline-block',
                    padding: 'var(--space-xs) var(--space-sm)',
                    backgroundColor: 'var(--color-primary)',
                    color: 'var(--color-background)',
                    borderRadius: 'var(--radius-sm)',
                    fontSize: 'var(--font-size-xs)',
                    marginBottom: 'var(--space-sm)'
                  }}>
                    Current Question
                  </div>
                  <h3 style={{ 
                    fontSize: 'var(--font-size-lg)',
                    marginBottom: 'var(--space-sm)',
                    color: 'var(--color-primary)'
                  }}>
                    Question {state.qa_chain.length + 1}
                  </h3>
                  <p style={{ lineHeight: '1.6' }}>
                    {state.last_question}
                  </p>
                  {loading && (
                    <div style={{ 
                      marginTop: 'var(--space-md)',
                      padding: 'var(--space-md)',
                      backgroundColor: 'var(--color-surface)',
                      borderRadius: 'var(--radius-md)',
                      textAlign: 'center'
                    }}>
                      <div style={{ 
                        display: 'inline-block',
                        width: '20px',
                        height: '20px',
                        border: '2px solid var(--color-border)',
                        borderTopColor: 'var(--color-primary)',
                        borderRadius: '50%',
                        animation: 'spin 1s linear infinite'
                      }} />
                      <style jsx>{`
                        @keyframes spin {
                          to { transform: rotate(360deg); }
                        }
                      `}</style>
                      <p style={{ marginTop: 'var(--space-sm)', fontSize: 'var(--font-size-sm)' }}>
                        Generating answer...
                      </p>
                    </div>
                  )}
                </Card>
              )}

              {/* Show current answer if exists but no next question yet */}
              {state.last_answer && state.last_question && (
                <Card variant="default">
                  <div style={{ 
                    display: 'inline-block',
                    padding: 'var(--space-xs) var(--space-sm)',
                    backgroundColor: 'var(--color-surface)',
                    borderRadius: 'var(--radius-sm)',
                    fontSize: 'var(--font-size-xs)',
                    marginBottom: 'var(--space-sm)'
                  }}>
                    Latest Answer
                  </div>
                  <h4 style={{ 
                    fontSize: 'var(--font-size-base)',
                    marginBottom: 'var(--space-sm)',
                    color: 'var(--color-text-secondary)'
                  }}>
                    Answer {state.qa_chain.length + 1}
                  </h4>
                  <p style={{ 
                    lineHeight: '1.8',
                    whiteSpace: 'pre-wrap',
                    marginBottom: 'var(--space-md)'
                  }}>
                    {state.last_answer}
                  </p>
                  {loading && (
                    <div style={{ 
                      padding: 'var(--space-md)',
                      backgroundColor: 'var(--color-surface)',
                      borderRadius: 'var(--radius-md)',
                      textAlign: 'center'
                    }}>
                      <div style={{ 
                        display: 'inline-block',
                        width: '20px',
                        height: '20px',
                        border: '2px solid var(--color-border)',
                        borderTopColor: 'var(--color-primary)',
                        borderRadius: '50%',
                        animation: 'spin 1s linear infinite'
                      }} />
                      <p style={{ marginTop: 'var(--space-sm)', fontSize: 'var(--font-size-sm)' }}>
                        Generating next question...
                      </p>
                    </div>
                  )}
                </Card>
              )}
            </div>
          )}
        </div>

        {/* Generate Next Button */}
        <div style={{ 
          position: 'sticky',
          bottom: 'var(--space-lg)',
          display: 'flex',
          justifyContent: 'center',
          marginTop: 'var(--space-xl)'
        }}>
          <Card variant="default" style={{ 
            padding: 'var(--space-lg)',
            boxShadow: 'var(--shadow-lg)'
          }}>
            <Button
              variant="primary"
              onClick={handleGenerateNext}
              disabled={loading}
              style={{ 
                fontSize: 'var(--font-size-lg)',
                padding: 'var(--space-md) var(--space-xl)'
              }}
            >
              {loading ? 'Generating...' : 'Generate Next'}
            </Button>
            <p style={{ 
              marginTop: 'var(--space-sm)',
              fontSize: 'var(--font-size-xs)',
              color: 'var(--color-text-secondary)',
              textAlign: 'center'
            }}>
              {state?.last_question && !state?.last_answer 
                ? 'Generating answer for current question...'
                : state?.last_answer
                ? 'Generating next question from answer...'
                : 'Starting generation chain...'}
            </p>
          </Card>
        </div>
      </article>
    </main>
  );
}

