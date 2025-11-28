'use client'

import { useState, useEffect, Suspense } from 'react'
import { signIn, useSession } from 'next-auth/react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Card, Button } from '@kushalsamant/design-template'
import Link from 'next/link'

function SignInContent() {
  const [termsAccepted, setTermsAccepted] = useState(false)
  const [ageVerified, setAgeVerified] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const router = useRouter()
  const searchParams = useSearchParams()
  const { data: session, status } = useSession()

  const canSubmit = termsAccepted && ageVerified && !isSubmitting

  useEffect(() => {
    if (status === 'authenticated') {
      const callbackUrl = searchParams?.get('callbackUrl') || '/'
      router.push(callbackUrl)
    }
  }, [status, router, searchParams])

  const handleSignIn = async () => {
    if (!canSubmit) return
    
    setIsSubmitting(true)
    try {
      await signIn('google', { callbackUrl: '/' })
    } catch (error) {
      console.error('Sign in error:', error)
      setIsSubmitting(false)
    }
  }

  if (status === 'loading') {
    return <div className="p-8">Loading...</div>
  }

  if (status === 'authenticated') {
    return null
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 'var(--space-md)' }}>
      <Card variant="default" style={{ maxWidth: '28rem', width: '100%' }}>
        <div style={{ padding: 'var(--space-xl)', display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
          <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
            <h1 style={{ fontSize: 'var(--font-size-3xl)', fontWeight: 'var(--font-weight-bold)' }}>Welcome to ASK</h1>
            <p style={{ color: 'var(--color-text-secondary)' }}>
              Sign in to browse and generate research Q&A pairs
            </p>
          </div>

          <div style={{ padding: 'var(--space-md)', backgroundColor: 'var(--color-surface)', borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)', display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: 'var(--space-sm)' }}>
              <input
                type="checkbox"
                id="age-verification"
                checked={ageVerified}
                onChange={(e) => setAgeVerified(e.target.checked)}
                style={{ marginTop: '0.25rem' }}
              />
              <label htmlFor="age-verification" style={{ fontSize: 'var(--font-size-sm)' }}>
                I am at least 13 years old
              </label>
            </div>
            <div style={{ display: 'flex', alignItems: 'flex-start', gap: 'var(--space-sm)' }}>
              <input
                type="checkbox"
                id="terms-acceptance"
                checked={termsAccepted}
                onChange={(e) => setTermsAccepted(e.target.checked)}
                style={{ marginTop: '0.25rem' }}
              />
              <label htmlFor="terms-acceptance" style={{ fontSize: 'var(--font-size-sm)' }}>
                I agree to the{' '}
                <Link href="https://kvshvl.in/termsofservice" target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'underline' }}>
                  Terms of Service
                </Link>
                {' '}and{' '}
                <Link href="https://kvshvl.in/privacypolicy" target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'underline' }}>
                  Privacy Policy
                </Link>
              </label>
            </div>
          </div>

          <Button
            variant="primary"
            onClick={handleSignIn}
            disabled={!canSubmit}
            style={{ width: '100%' }}
          >
            {isSubmitting ? 'Signing in...' : 'Sign in with Google'}
          </Button>
        </div>
      </Card>
    </div>
  )
}

export default function SignInPage() {
  return (
    <Suspense fallback={<div className="p-8">Loading...</div>}>
      <SignInContent />
    </Suspense>
  )
}

