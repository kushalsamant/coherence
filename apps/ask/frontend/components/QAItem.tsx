'use client';

import Link from 'next/link';
import { Card } from '@kushalsamant/design-template';
import { QAPair } from '@/lib/api';

interface QAItemProps {
  qaPair: QAPair;
}

export function QAItem({ qaPair }: QAItemProps) {
  return (
    <Card variant="default" hover>
      <Link href={`/qa/${qaPair.question_number}`} style={{ textDecoration: 'none', color: 'inherit' }}>
        <div style={{ marginBottom: 'var(--space-md)' }}>
          <div style={{ 
            display: 'inline-block', 
            padding: 'var(--space-xs) var(--space-sm)', 
            backgroundColor: 'var(--color-surface)', 
            borderRadius: 'var(--radius-sm)',
            fontSize: 'var(--font-size-xs)',
            marginBottom: 'var(--space-sm)'
          }}>
            {qaPair.theme}
          </div>
          <h3 style={{ 
            marginBottom: 'var(--space-sm)', 
            fontSize: 'var(--font-size-lg)',
            lineHeight: '1.4'
          }}>
            {qaPair.question}
          </h3>
          <p style={{ 
            color: 'var(--color-text-secondary)', 
            fontSize: 'var(--font-size-sm)',
            lineHeight: '1.6',
            display: '-webkit-box',
            WebkitLineClamp: 3,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden'
          }}>
            {qaPair.answer}
          </p>
          <div style={{ 
            marginTop: 'var(--space-md)', 
            fontSize: 'var(--font-size-xs)', 
            color: 'var(--color-text-tertiary)' 
          }}>
            ASK-{qaPair.question_number.toString().padStart(3, '0')}
          </div>
        </div>
      </Link>
    </Card>
  );
}

