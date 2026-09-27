'use client'

import { useState } from 'react'

export default function IntegrationsPage() {
  const [integrations, setIntegrations] = useState<any[]>([])

  const availableIntegrations = [
    { name: 'Slack', icon: '💬', desc: 'Send notifications to Slack' },
    { name: 'Zapier', icon: '⚡', desc: 'Automate workflows' },
    { name: 'Stripe', icon: '💳', desc: 'Process payments' },
    { name: 'SendGrid', icon: '📧', desc: 'Email delivery' },
    { name: 'Twilio', icon: '📱', desc: 'SMS messages' },
  ]

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Integrations</h1>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Connected Integrations</h2>
        {integrations.length === 0 ? (
          <div className="text-gray-600">No integrations connected yet.</div>
        ) : (
          <div className="space-y-2">
            {integrations.map((int) => (
              <div key={int.id} className="p-3 bg-green-50 rounded border border-green-200">
                ✓ {int.name}
              </div>
            ))}
          </div>
        )}
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-4">Available Integrations</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {availableIntegrations.map((integ) => (
            <div key={integ.name} className="bg-white rounded-lg shadow p-6 hover:shadow-lg cursor-pointer">
              <div className="text-4xl mb-2">{integ.icon}</div>
              <h3 className="font-semibold">{integ.name}</h3>
              <p className="text-sm text-gray-600 mb-4">{integ.desc}</p>
              <button className="text-blue-600 hover:underline text-sm">Connect</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
