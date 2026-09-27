'use client'

import { useState } from 'react'

export default function PermissionsPage() {
  const [resources, setResources] = useState([
    { id: 1, type: 'video', name: 'Tutorial 1', permissions: 'edit' },
    { id: 2, type: 'article', name: 'Guide 2', permissions: 'view' },
  ])
  const [selectedUser, setSelectedUser] = useState('')
  const [selectedLevel, setSelectedLevel] = useState('view')

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Permissions</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-sm font-semibold">Resource</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold">Type</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold">Permission</th>
                  <th className="px-6 py-3 text-left text-sm font-semibold">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {resources.map((r) => (
                  <tr key={r.id} className="hover:bg-gray-50">
                    <td className="px-6 py-3 text-sm">{r.name}</td>
                    <td className="px-6 py-3 text-sm text-gray-600">{r.type}</td>
                    <td className="px-6 py-3 text-sm">
                      <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                        {r.permissions}
                      </span>
                    </td>
                    <td className="px-6 py-3 text-sm">
                      <button className="text-blue-600 hover:underline">Edit</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Grant Access</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">User Email</label>
              <input
                type="email"
                value={selectedUser}
                onChange={(e) => setSelectedUser(e.target.value)}
                className="w-full px-3 py-2 border rounded-md"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Permission</label>
              <select value={selectedLevel} onChange={(e) => setSelectedLevel(e.target.value)} className="w-full px-3 py-2 border rounded-md">
                <option value="view">View</option>
                <option value="comment">Comment</option>
                <option value="edit">Edit</option>
                <option value="manage">Manage</option>
              </select>
            </div>
            <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">Grant</button>
          </div>
        </div>
      </div>
    </div>
  )
}
