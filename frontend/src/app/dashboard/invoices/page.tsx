'use client'

import { useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface Invoice {
  id: number
  amount: number
  status: string
  due_date: string | null
  paid_date: string | null
  created_at: string | null
}

/** Invoices of the signed-in user's current subscription. */
export default function InvoicesPage() {
  const [hasSubscription, setHasSubscription] = useState<boolean | null>(null)
  const [invoices, setInvoices] = useState<Invoice[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    ApiClient.get('/monetization/subscriptions/current')
      .then(() => {
        setHasSubscription(true);
        return ApiClient.get('/monetization/invoices');
      })
      .then((data: Invoice[]) => setInvoices(Array.isArray(data) ? data : []))
      .catch((err) => {
        if (err instanceof Error && err.message === 'No active subscription') {
          setHasSubscription(false);
          setInvoices([]);
        } else {
          setError(errorMessage(err, 'Invoices could not be loaded.'));
        }
      });
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Invoices</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}

      <div className="bg-white rounded-lg shadow p-6">
        {invoices === null && !error ? (
          <p className="text-gray-500">Loading invoices…</p>
        ) : hasSubscription === false ? (
          <p className="text-gray-500">You have no active subscription, so there are no invoices.</p>
        ) : invoices && invoices.length === 0 ? (
          <p className="text-gray-500">No invoices yet.</p>
        ) : invoices ? (
          <table className="min-w-full text-sm">
            <thead className="text-left text-gray-600">
              <tr>
                <th className="py-2">Invoice</th>
                <th className="py-2">Amount</th>
                <th className="py-2">Status</th>
                <th className="py-2">Due</th>
                <th className="py-2">Paid</th>
              </tr>
            </thead>
            <tbody>
              {invoices.map((invoice) => (
                <tr key={invoice.id} className="border-t">
                  <td className="py-2">#{invoice.id}</td>
                  <td className="py-2">${invoice.amount.toFixed(2)}</td>
                  <td className="py-2">{invoice.status}</td>
                  <td className="py-2">{invoice.due_date ? new Date(invoice.due_date).toLocaleDateString() : '—'}</td>
                  <td className="py-2">{invoice.paid_date ? new Date(invoice.paid_date).toLocaleDateString() : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : null}
      </div>
    </div>
  );
}
