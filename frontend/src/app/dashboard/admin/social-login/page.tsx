'use client'

import { useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { ApiClient } from '@/lib/api-client'

export interface SocialProviderAdminView {
  provider: string
  display_name: string
  enabled: boolean
  client_id: string | null
  client_secret_set: boolean
  redirect_uri: string | null
  scopes: string
  updated_at: string | null
}

interface Draft {
  enabled: boolean
  client_id: string
  client_secret: string
  redirect_uri: string
  scopes: string
}

type Feedback = { kind: 'success' | 'error'; text: string }

function toDraft(view: SocialProviderAdminView): Draft {
  return {
    enabled: view.enabled,
    client_id: view.client_id ?? '',
    client_secret: '',
    redirect_uri: view.redirect_uri ?? '',
    scopes: view.scopes ?? '',
  }
}

/** Administrators manage the OAuth client credentials used for social sign-in. */
export default function SocialLoginAdminPage() {
  const [providers, setProviders] = useState<SocialProviderAdminView[]>([])
  const [drafts, setDrafts] = useState<Record<string, Draft>>({})
  const [saving, setSaving] = useState<string | null>(null)
  const [feedback, setFeedback] = useState<Record<string, Feedback>>({})
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState('')

  useEffect(() => {
    ApiClient.get('/admin/social-providers')
      .then((list: SocialProviderAdminView[]) => {
        setProviders(list)
        setDrafts(Object.fromEntries(list.map((item) => [item.provider, toDraft(item)])))
      })
      .catch((err: Error) => setLoadError(err.message || 'Could not load social login providers'))
      .finally(() => setLoading(false))
  }, [])

  const updateDraft = (provider: string, changes: Partial<Draft>) => {
    setDrafts((current) => ({ ...current, [provider]: { ...current[provider], ...changes } }))
  }

  const save = async (view: SocialProviderAdminView) => {
    const draft = drafts[view.provider]
    setSaving(view.provider)
    setFeedback(({ [view.provider]: _cleared, ...rest }) => rest)
    try {
      const body: Record<string, unknown> = {
        enabled: draft.enabled,
        client_id: draft.client_id,
        redirect_uri: draft.redirect_uri,
        scopes: draft.scopes,
      }
      // The secret is write-only: send it only when the administrator typed a new one.
      if (draft.client_secret) {
        body.client_secret = draft.client_secret
      }
      const updated: SocialProviderAdminView = await ApiClient.put(
        `/admin/social-providers/${view.provider}`,
        body,
      )
      setProviders((current) => current.map((item) => (item.provider === updated.provider ? updated : item)))
      setDrafts((current) => ({ ...current, [updated.provider]: toDraft(updated) }))
      setFeedback((current) => ({ ...current, [view.provider]: { kind: 'success', text: 'Saved.' } }))
    } catch (err: any) {
      setFeedback((current) => ({
        ...current,
        [view.provider]: { kind: 'error', text: err.message || 'Could not save these settings' },
      }))
    } finally {
      setSaving(null)
    }
  }

  if (loading) {
    return <p className="p-6 text-sm text-gray-600" role="status">Loading social login providers...</p>
  }
  if (loadError) {
    return <p role="alert" className="p-6 text-sm text-red-700">{loadError}</p>
  }

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">Social login</h1>
        <p className="mt-1 text-sm text-gray-600">
          OAuth client credentials for sign-in with external accounts. Register the redirect URI below with each
          provider as <code>{'{your-frontend}/auth/social/{provider}/callback'}</code>.
        </p>
      </div>

      {providers.map((view) => {
        const draft = drafts[view.provider]
        if (!draft) return null
        const message = feedback[view.provider]
        const fieldId = (name: string) => `${view.provider}-${name}`
        return (
          <Card key={view.provider}>
            <CardHeader>
              <CardTitle>{view.display_name}</CardTitle>
              <CardDescription>
                {view.enabled ? 'Enabled: shown on the sign-in page' : 'Disabled: hidden from the sign-in page'}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
                <Checkbox
                  id={fieldId('enabled')}
                  checked={draft.enabled}
                  onCheckedChange={(checked: boolean) => updateDraft(view.provider, { enabled: checked })}
                />
                Enable {view.display_name} sign-in
              </label>

              <div className="grid gap-4 md:grid-cols-2">
                <div>
                  <label htmlFor={fieldId('client-id')} className="block text-sm font-medium text-gray-700">
                    Client ID
                  </label>
                  <Input
                    id={fieldId('client-id')}
                    value={draft.client_id}
                    onChange={(e) => updateDraft(view.provider, { client_id: e.target.value })}
                    maxLength={255}
                  />
                </div>
                <div>
                  <label htmlFor={fieldId('client-secret')} className="block text-sm font-medium text-gray-700">
                    Client secret
                  </label>
                  <Input
                    id={fieldId('client-secret')}
                    type="password"
                    autoComplete="new-password"
                    value={draft.client_secret}
                    placeholder={view.client_secret_set ? 'Stored. Type a new value to replace it.' : 'Not set'}
                    onChange={(e) => updateDraft(view.provider, { client_secret: e.target.value })}
                    maxLength={512}
                  />
                </div>
                <div>
                  <label htmlFor={fieldId('redirect-uri')} className="block text-sm font-medium text-gray-700">
                    Redirect URI
                  </label>
                  <Input
                    id={fieldId('redirect-uri')}
                    value={draft.redirect_uri}
                    onChange={(e) => updateDraft(view.provider, { redirect_uri: e.target.value })}
                    maxLength={500}
                  />
                </div>
                <div>
                  <label htmlFor={fieldId('scopes')} className="block text-sm font-medium text-gray-700">
                    Scopes
                  </label>
                  <Input
                    id={fieldId('scopes')}
                    value={draft.scopes}
                    onChange={(e) => updateDraft(view.provider, { scopes: e.target.value })}
                    maxLength={500}
                  />
                </div>
              </div>

              <div className="flex items-center gap-3">
                <Button onClick={() => save(view)} disabled={saving === view.provider}>
                  {saving === view.provider ? 'Saving...' : 'Save'}
                </Button>
                {message && (
                  <p role={message.kind === 'error' ? 'alert' : 'status'}
                    className={message.kind === 'error' ? 'text-sm text-red-700' : 'text-sm text-green-700'}>
                    {message.text}
                  </p>
                )}
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
