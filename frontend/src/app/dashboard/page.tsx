'use client'

import { useAuth } from '@/hooks/useAuth'
import Link from 'next/link'

export default function DashboardPage() {
  const { user } = useAuth()

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Welcome, {user?.name}!</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-blue-600">0</div>
          <div className="text-gray-600">Videos</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-green-600">0</div>
          <div className="text-gray-600">Articles</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-purple-600">0</div>
          <div className="text-gray-600">Chats</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-3xl font-bold text-orange-600">$0</div>
          <div className="text-gray-600">Monthly Spend</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
          <div className="space-y-2">
            <Link href="/dashboard/content" className="block p-3 bg-blue-50 rounded hover:bg-blue-100">
              📹 Manage Content
            </Link>
            <Link href="/dashboard/ai" className="block p-3 bg-purple-50 rounded hover:bg-purple-100">
              🤖 AI Features
            </Link>
            <Link href="/dashboard/analytics" className="block p-3 bg-green-50 rounded hover:bg-green-100">
              📈 View Analytics
            </Link>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
          <div className="text-gray-600">No recent activity yet.</div>
        </div>
      </div>
    </div>
  )
}
