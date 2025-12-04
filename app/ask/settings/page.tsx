'use client'

import { useEffect, useState } from 'react'
import { useSession, signOut } from '@/lib/auth-provider'
import { useRouter } from 'next/navigation'
import { Card, Button } from '@kushalsamant/design-template'

export default function SettingsPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (status !== 'loading') {
      if (!session) {
        router.push('/sign-in')
      } else {
        setLoading(false)
      }
    }
  }, [session, status, router])

  if (status === 'loading' || loading) {
    return <div className="p-8">Loading...</div>
  }

  if (!session) {
    return null
  }

  return (
    <div style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <div style={{ marginBottom: 'var(--space-2xl)' }}>
        <h1 style={{ fontSize: 'var(--font-size-4xl)', fontWeight: 'var(--font-weight-bold)', marginBottom: 'var(--space-lg)' }}>
          Settings
        </h1>
        <p style={{ fontSize: 'var(--font-size-lg)', color: 'var(--color-text-secondary)' }}>
          Manage your account settings
        </p>
      </div>

      <Card variant="default" style={{ marginBottom: 'var(--space-lg)' }}>
        <div style={{ padding: 'var(--space-xl)' }}>
          <h2 style={{ fontSize: 'var(--font-size-xl)', fontWeight: 'var(--font-weight-bold)', marginBottom: 'var(--space-md)' }}>
            Account Information
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
            <div>
              <strong>Email:</strong> {session.user?.email}
            </div>
            {session.user?.name && (
              <div>
                <strong>Name:</strong> {session.user.name}
              </div>
            )}
          </div>
        </div>
      </Card>

      <Card variant="default">
        <div style={{ padding: 'var(--space-xl)' }}>
          <h2 style={{ fontSize: 'var(--font-size-xl)', fontWeight: 'var(--font-weight-bold)', marginBottom: 'var(--space-md)' }}>
            Actions
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
            <Button
              variant="primary"
              onClick={() => signOut({ callbackUrl: '/' })}
            >
              Sign Out
            </Button>
          </div>
        </div>
      </Card>
    </div>
  )
}

