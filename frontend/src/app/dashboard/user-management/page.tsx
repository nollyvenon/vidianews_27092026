'use client'

import { FormEvent, useEffect, useState } from 'react'
import { Users, Mail, TrendingUp, Bell, Zap } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface Overview {
  total_subscribers: number
  new_subscribers_this_month: number
  average_engagement: number
  average_churn_risk: number
  tiers: { tier: string; count: number }[]
  engagement_levels: { level: string; count: number }[]
  churn_risk_levels: { level: string; count: number }[]
  campaigns_sent: number
  campaigns_sent_last_7_days: number
  active_segments: number
  dynamic_segments: number
}

interface Campaign {
  id: number
  name: string
  status: string | null
  sent_count: number
  open_count: number
  click_count: number
  ctr: number
  sent_at: string | null
}

interface ApiKey {
  id: number
  name: string
  permissions: string[]
  is_active: boolean
  key_suffix: string
}

const ENGAGEMENT_LABELS: Record<string, { label: string; color: string }> = {
  highly_engaged: { label: 'Highly Engaged', color: 'bg-green-600' },
  engaged: { label: 'Engaged', color: 'bg-blue-600' },
  low_engagement: { label: 'Low Engagement', color: 'bg-orange-600' },
  inactive: { label: 'Inactive', color: 'bg-red-600' },
}

const CHURN_LABELS: Record<string, { risk: string; action: string }> = {
  high: { risk: 'High Risk (>80%)', action: 'Urgent outreach' },
  medium: { risk: 'Medium Risk (50-80%)', action: 'Engagement campaign' },
  low: { risk: 'Low Risk (<50%)', action: 'Monitor' },
}

const ERROR_CLASS = 'bg-red-50 border border-red-200 text-red-700 rounded-md p-3'

const percentOf = (count: number, total: number) => (total > 0 ? Math.round((count / total) * 1000) / 10 : 0)

const capitalise = (value: string) => value.charAt(0).toUpperCase() + value.slice(1)

/** Subscriber dashboard figures, campaign performance, and the API keys and webhooks used to integrate. */
export default function UserManagementPage() {
  const [overview, setOverview] = useState<Overview | null>(null)
  const [overviewError, setOverviewError] = useState<string | null>(null)
  const [campaigns, setCampaigns] = useState<Campaign[] | null>(null)
  const [campaignsError, setCampaignsError] = useState<string | null>(null)

  const [keys, setKeys] = useState<ApiKey[] | null>(null)
  const [actionError, setActionError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)
  const [keyName, setKeyName] = useState('')
  const [keyPermissions, setKeyPermissions] = useState('read')
  const [issued, setIssued] = useState<string | null>(null)
  const [hookName, setHookName] = useState('')
  const [hookUrl, setHookUrl] = useState('')
  const [hookEvents, setHookEvents] = useState('content.published')
  const [hookSecret, setHookSecret] = useState<{ id: number; secret: string } | null>(null)
  const [hookId, setHookId] = useState('')
  const [hookEvent, setHookEvent] = useState('content.published')
  const [delivery, setDelivery] = useState<string | null>(null)

  const loadKeys = () =>
    ApiClient.get('/api-keys/')
      .then((data: ApiKey[]) => setKeys(Array.isArray(data) ? data : []))
      .catch((err) => setActionError(errorMessage(err, 'API keys could not be loaded.')));

  useEffect(() => {
    ApiClient.get('/subscribers/overview')
      .then((data: Overview) => setOverview(data))
      .catch((err) => setOverviewError(errorMessage(err, 'Subscriber figures could not be loaded.')));
    ApiClient.get('/emails/campaigns?limit=10')
      .then((data: Campaign[]) => setCampaigns(Array.isArray(data) ? data : []))
      .catch((err) => setCampaignsError(errorMessage(err, 'Campaign performance could not be loaded.')));
    loadKeys();
  }, []);

  const createKey = async (event: FormEvent) => {
    event.preventDefault();
    setActionError(null);
    setIssued(null);
    try {
      const result: { key: string } = await ApiClient.post('/api-keys/', {
        name: keyName.trim(),
        permissions: keyPermissions.split(',').map((item) => item.trim()).filter(Boolean),
      });
      setIssued(result.key);
      setKeyName('');
      await loadKeys();
    } catch (err) {
      setActionError(errorMessage(err, 'The API key could not be created.'));
    }
  };

  const revokeKey = async (key: ApiKey) => {
    setActionError(null);
    try {
      await ApiClient.delete(`/api-keys/${key.id}`);
      setNotice(`"${key.name}" was revoked.`);
      await loadKeys();
    } catch (err) {
      setActionError(errorMessage(err, 'The API key could not be revoked.'));
    }
  };

  const createHook = async (event: FormEvent) => {
    event.preventDefault();
    setActionError(null);
    setHookSecret(null);
    try {
      const result: { id: number; secret_key: string } = await ApiClient.post('/webhooks/endpoints', {
        name: hookName.trim(),
        url: hookUrl.trim(),
        events: hookEvents.split(',').map((item) => item.trim()).filter(Boolean),
      });
      setHookSecret({ id: result.id, secret: result.secret_key });
      setHookName('');
      setHookUrl('');
    } catch (err) {
      setActionError(errorMessage(err, 'The webhook endpoint could not be registered.'));
    }
  };

  const triggerHook = async (event: FormEvent) => {
    event.preventDefault();
    setActionError(null);
    setDelivery(null);
    try {
      const result: { delivered: boolean; status_code: number | null; error: string | null } = await ApiClient.post(
        `/webhooks/${Number(hookId)}/trigger`,
        { event_type: hookEvent.trim(), payload: {} },
      );
      if (result.delivered) {
        setDelivery(`Delivered to webhook ${hookId} (HTTP ${result.status_code}).`);
      } else if (result.status_code !== null) {
        setDelivery(`Webhook ${hookId} responded with HTTP ${result.status_code}; it is not marked delivered.`);
      } else {
        setDelivery(`Webhook ${hookId} could not be reached: ${result.error ?? 'unknown error'}.`);
      }
    } catch (err) {
      setActionError(errorMessage(err, 'The event could not be sent.'));
    }
  };

  const total = overview?.total_subscribers ?? 0;
  const engagementLevels = overview?.engagement_levels ?? [];
  const churnLevels = overview?.churn_risk_levels ?? [];

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">User Management</h1>
      {overviewError && <p role="alert" className={ERROR_CLASS}>{overviewError}</p>}
      {campaignsError && <p role="alert" className={ERROR_CLASS}>{campaignsError}</p>}
      {actionError && <p role="alert" className={ERROR_CLASS}>{actionError}</p>}
      {notice && <p role="status" className="text-green-700">{notice}</p>}

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Users className="h-4 w-4" />
              Total Subscribers
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{overview ? total.toLocaleString() : '—'}</div>
            <p className="text-xs text-gray-500">{overview ? `+${overview.new_subscribers_this_month.toLocaleString()} this month` : 'Loading…'}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Mail className="h-4 w-4" />
              Campaigns Sent
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{overview ? overview.campaigns_sent.toLocaleString() : '—'}</div>
            <p className="text-xs text-gray-500">{overview ? `${overview.campaigns_sent_last_7_days} in last 7 days` : 'Loading…'}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm">
              <TrendingUp className="h-4 w-4" />
              Avg Engagement
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{overview ? `${overview.average_engagement}%` : '—'}</div>
            <p className="text-xs text-gray-500">Average engagement score</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Bell className="h-4 w-4" />
              Active Segments
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{overview ? overview.active_segments.toLocaleString() : '—'}</div>
            <p className="text-xs text-gray-500">{overview ? `${overview.dynamic_segments} rule-based segments` : 'Loading…'}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Zap className="h-4 w-4" />
              Churn Risk
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{overview ? `${(overview.average_churn_risk * 100).toFixed(1)}%` : '—'}</div>
            <p className="text-xs text-gray-500">Average churn probability</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Subscriber Tiers */}
        <Card>
          <CardHeader>
            <CardTitle>Subscriber Distribution</CardTitle>
            <CardDescription>By subscription tier</CardDescription>
          </CardHeader>
          <CardContent>
            {!overview ? (
              <p className="text-gray-500">Loading tiers…</p>
            ) : overview.tiers.length === 0 ? (
              <p className="text-gray-500">No subscribers yet.</p>
            ) : (
              <div className="space-y-4">
                {overview.tiers.map((item) => (
                  <div key={item.tier} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="font-medium">{capitalise(item.tier)}</span>
                      <span className="text-gray-600">{item.count.toLocaleString()}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${percentOf(item.count, total)}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Engagement Score Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Engagement Levels</CardTitle>
            <CardDescription>Subscriber segments by engagement</CardDescription>
          </CardHeader>
          <CardContent>
            {!overview ? (
              <p className="text-gray-500">Loading engagement…</p>
            ) : (
              <div className="space-y-3">
                {engagementLevels.map((item) => (
                  <div key={item.level} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className={`w-3 h-3 rounded-full ${ENGAGEMENT_LABELS[item.level]?.color ?? 'bg-gray-400'}`}></div>
                      <span className="text-sm">{ENGAGEMENT_LABELS[item.level]?.label ?? item.level}</span>
                    </div>
                    <span className="text-sm font-medium">{item.count.toLocaleString()}</span>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Campaign Performance */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Campaigns</CardTitle>
          <CardDescription>Email campaign performance</CardDescription>
        </CardHeader>
        <CardContent>
          {campaigns === null && !campaignsError ? (
            <p className="text-gray-500">Loading campaigns…</p>
          ) : campaigns && campaigns.length === 0 ? (
            <p className="text-gray-500">No campaigns sent yet.</p>
          ) : campaigns ? (
            <div className="space-y-3">
              {campaigns.map((campaign) => (
                <div key={campaign.id} className="border rounded-lg p-3">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <p className="font-medium text-sm">{campaign.name}</p>
                      <p className="text-xs text-gray-600">Sent to {campaign.sent_count.toLocaleString()}</p>
                    </div>
                    <span className="text-sm font-semibold text-green-600">{campaign.ctr}% CTR</span>
                  </div>
                  <div className="flex gap-4 text-xs">
                    <span className="text-gray-600">Opens: {campaign.open_count.toLocaleString()}</span>
                    <span className="text-gray-600">Clicks: {campaign.click_count.toLocaleString()}</span>
                  </div>
                </div>
              ))}
            </div>
          ) : null}
        </CardContent>
      </Card>

      {/* Churn Risk */}
      <Card>
        <CardHeader>
          <CardTitle>At-Risk Subscribers</CardTitle>
          <CardDescription>Users likely to churn in next 30 days</CardDescription>
        </CardHeader>
        <CardContent>
          {!overview ? (
            <p className="text-gray-500">Loading risk groups…</p>
          ) : (
            <div className="space-y-2">
              {churnLevels.map((item) => (
                <div key={item.level} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                  <div>
                    <p className="font-medium text-sm">{CHURN_LABELS[item.level]?.risk ?? item.level}</p>
                    <p className="text-xs text-gray-600">{item.count.toLocaleString()} subscribers</p>
                  </div>
                  <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                    {CHURN_LABELS[item.level]?.action ?? 'Review'}
                  </span>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* API keys */}
      <Card>
        <CardHeader>
          <CardTitle>API keys</CardTitle>
          <CardDescription>Keys that let your integrations call the platform as you</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {keys === null ? (
            <p className="text-gray-500">Loading keys…</p>
          ) : keys.length === 0 ? (
            <p className="text-gray-500">No API keys yet.</p>
          ) : (
            <ul className="space-y-2">
              {keys.map((key) => (
                <li key={key.id} className="border rounded p-3 flex justify-between items-center">
                  <span>
                    <span className="font-medium">{key.name}</span> · ends …{key.key_suffix} · {key.permissions.join(', ') || 'no permissions'}
                    {!key.is_active && <span className="ml-2 text-gray-500">(revoked)</span>}
                  </span>
                  {key.is_active && (
                    <button type="button" onClick={() => revokeKey(key)} className="text-sm text-red-600 hover:underline">Revoke</button>
                  )}
                </li>
              ))}
            </ul>
          )}
          {issued && (
            <div role="status" className="border border-yellow-300 bg-yellow-50 rounded p-3 text-sm">
              Copy this key now. It is shown only once: <code className="font-mono break-all">{issued}</code>
            </div>
          )}
          <form onSubmit={createKey} className="flex flex-wrap gap-2 items-end">
            <input className="border rounded px-2 py-1" placeholder="Key name" value={keyName} onChange={(e) => setKeyName(e.target.value)} required />
            <input className="border rounded px-2 py-1" placeholder="Permissions (comma separated)" value={keyPermissions} onChange={(e) => setKeyPermissions(e.target.value)} />
            <button type="submit" disabled={!keyName.trim()} className="px-3 py-1 bg-blue-600 text-white rounded disabled:opacity-50">Create API key</button>
          </form>
        </CardContent>
      </Card>

      {/* Webhooks */}
      <Card>
        <CardHeader>
          <CardTitle>Webhook endpoints</CardTitle>
          <CardDescription>Receive platform events at your own URL, signed with a secret</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {hookSecret && (
            <div role="status" className="border border-yellow-300 bg-yellow-50 rounded p-3 text-sm">
              Endpoint {hookSecret.id} is registered. Save this signing secret now; it is shown only once and
              verifies the X-Webhook-Signature header: <code className="font-mono break-all">{hookSecret.secret}</code>
            </div>
          )}
          <form onSubmit={createHook} className="grid grid-cols-1 md:grid-cols-2 gap-2">
            <input className="border rounded px-2 py-1" placeholder="Endpoint name" value={hookName} onChange={(e) => setHookName(e.target.value)} required />
            <input className="border rounded px-2 py-1" type="url" placeholder="https://example.com/hook" value={hookUrl} onChange={(e) => setHookUrl(e.target.value)} required />
            <input className="border rounded px-2 py-1 md:col-span-2" placeholder="Events (comma separated)" value={hookEvents} onChange={(e) => setHookEvents(e.target.value)} />
            <button type="submit" disabled={!hookName.trim() || !hookUrl.trim()} className="px-3 py-1 bg-blue-600 text-white rounded disabled:opacity-50 md:col-span-2">Register endpoint</button>
          </form>
          <form onSubmit={triggerHook} className="flex flex-wrap gap-2 items-end">
            <label className="text-sm">
              <span className="block text-xs text-gray-600">Endpoint ID</span>
              <input type="number" min={1} className="border rounded px-2 py-1" value={hookId} onChange={(e) => setHookId(e.target.value)} required />
            </label>
            <label className="text-sm">
              <span className="block text-xs text-gray-600">Event</span>
              <input className="border rounded px-2 py-1" value={hookEvent} onChange={(e) => setHookEvent(e.target.value)} required />
            </label>
            <button type="submit" disabled={!hookId} className="px-3 py-1 border border-blue-600 text-blue-600 rounded disabled:opacity-50">Send test event</button>
          </form>
          {delivery && <p role="status" className="text-sm">{delivery}</p>}
        </CardContent>
      </Card>
    </div>
  );
}
