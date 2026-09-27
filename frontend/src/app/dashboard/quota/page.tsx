'use client'

import { useState } from 'react'

export default function QuotaPage() {
  const [quotas] = useState({
    apiCalls: { used: 8500, limit: 10000, percentage: 85 },
    storage: { used: 450, limit: 1000, percentage: 45 },
    bandwidth: { used: 280, limit: 500, percentage: 56 }
  })

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Usage & Quotas</h1>

      <div className="grid gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-6">Current Plan: Pro</h2>
          <div className="space-y-6">
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="font-medium">API Calls</label>
                <span className="text-sm text-gray-600">{quotas.apiCalls.used} / {quotas.apiCalls.limit}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-blue-600 h-3 rounded-full"
                  style={{ width: `${quotas.apiCalls.percentage}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">{quotas.apiCalls.percentage}% used</p>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="font-medium">Storage</label>
                <span className="text-sm text-gray-600">{quotas.storage.used}GB / {quotas.storage.limit}GB</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-green-600 h-3 rounded-full"
                  style={{ width: `${quotas.storage.percentage}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">{quotas.storage.percentage}% used</p>
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="font-medium">Bandwidth</label>
                <span className="text-sm text-gray-600">{quotas.bandwidth.used}GB / {quotas.bandwidth.limit}GB</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-yellow-600 h-3 rounded-full"
                  style={{ width: `${quotas.bandwidth.percentage}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1">{quotas.bandwidth.percentage}% used</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Upgrade Plans</h2>
          <div className="grid grid-cols-3 gap-4">
            <div className="border rounded-lg p-4 text-center">
              <p className="font-semibold">Basic</p>
              <p className="text-2xl font-bold text-blue-600 my-2">$29</p>
              <p className="text-sm text-gray-600">/month</p>
              <button className="w-full mt-3 px-3 py-2 border border-gray-300 rounded hover:bg-gray-50 text-sm">
                Current Plan
              </button>
            </div>
            <div className="border-2 border-blue-600 rounded-lg p-4 text-center bg-blue-50">
              <p className="font-semibold">Pro</p>
              <p className="text-2xl font-bold text-blue-600 my-2">$99</p>
              <p className="text-sm text-gray-600">/month</p>
              <button className="w-full mt-3 px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm">
                Current Plan
              </button>
            </div>
            <div className="border rounded-lg p-4 text-center">
              <p className="font-semibold">Enterprise</p>
              <p className="text-2xl font-bold text-blue-600 my-2">Custom</p>
              <p className="text-sm text-gray-600">Contact us</p>
              <button className="w-full mt-3 px-3 py-2 border border-gray-300 rounded hover:bg-gray-50 text-sm">
                Contact Sales
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
