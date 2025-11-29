'use client'

import { useEffect, useState } from 'react'
import { useSession, signOut } from 'next-auth/react'
import { useRouter } from 'next/navigation'
import { SettingsPage as SharedSettingsPage } from '@kvshvl/shared-frontend/settings'
import type { UserMetadata } from '@kvshvl/shared-frontend/settings'

export default function SettingsPage() {
  const { data: session, status } = useSession()
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [userMetadata, setUserMetadata] = useState<UserMetadata | null>(null)

  useEffect(() => {
    if (status !== 'loading') {
      if (!session) {
        router.push('/sign-in')
      } else {
        // Fetch user metadata from your API
        fetch('/api/user-metadata')
          .then(res => res.json())
          .then(data => {
            setUserMetadata({
              email: session.user?.email,
              name: session.user?.name,
              id: session.user?.id,
              ...data
            })
            setLoading(false)
          })
          .catch(() => {
            setUserMetadata({
              email: session.user?.email,
              name: session.user?.name,
              id: session.user?.id,
            })
            setLoading(false)
          })
      }
    }
  }, [session, status, router])

  if (status === 'loading' || loading) {
    return <div className="p-8">Loading...</div>
  }

  if (!session || !userMetadata) {
    return null
  }

  return (
    <SharedSettingsPage
      title="Settings"
      description="Manage your account settings"
      user={userMetadata}
      showProfile={true}
      showSubscription={true}
      showPaymentHistory={false}
      onSignOut={() => signOut({ callbackUrl: '/' })}
      apiEndpoints={{
        subscription: '/api/razorpay/subscriptions',
        paymentHistory: '/api/payments/history',
      }}
    />
  )
}

