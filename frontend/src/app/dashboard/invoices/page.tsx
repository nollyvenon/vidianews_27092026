'use client'

import { useState } from 'react'

export default function InvoicesPage() {
  const [invoices] = useState([
    { id: 'INV-001', date: '2026-09-27', amount: 99.00, status: 'paid', dueDate: '2026-09-27' },
    { id: 'INV-002', date: '2026-08-27', amount: 99.00, status: 'paid', dueDate: '2026-08-27' },
    { id: 'INV-003', date: '2026-07-27', amount: 99.00, status: 'paid', dueDate: '2026-07-27' },
    { id: 'INV-004', date: '2026-06-27', amount: 0, status: 'overdue', dueDate: '2026-06-27' }
  ])

  const totalRevenue = invoices.filter(i => i.status === 'paid').reduce((sum, i) => sum + i.amount, 0)

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Invoices</h1>

      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Total Revenue</p>
          <p className="text-2xl font-bold text-green-600">${totalRevenue.toFixed(2)}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Invoices This Year</p>
          <p className="text-2xl font-bold">{invoices.length}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Avg Invoice</p>
          <p className="text-2xl font-bold">${(totalRevenue / invoices.filter(i => i.status === 'paid').length).toFixed(2)}</p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b">
          <h2 className="text-xl font-semibold">Recent Invoices</h2>
        </div>
        <div className="divide-y">
          {invoices.map(inv => (
            <div key={inv.id} className="p-6 flex justify-between items-center hover:bg-gray-50">
              <div>
                <p className="font-semibold">{inv.id}</p>
                <p className="text-sm text-gray-600">{inv.date}</p>
              </div>
              <div className="text-right">
                <p className="font-semibold">${inv.amount.toFixed(2)}</p>
                <span className={`inline-block px-3 py-1 rounded text-sm text-white ${
                  inv.status === 'paid' ? 'bg-green-600' : 'bg-red-600'
                }`}>
                  {inv.status.charAt(0).toUpperCase() + inv.status.slice(1)}
                </span>
              </div>
              <button className="px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50">
                Download
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
