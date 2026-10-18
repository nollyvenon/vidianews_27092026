'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

export interface Coupon {
  id: number
  code: string
  discount_type: 'percent' | 'fixed'
  discount_value: number
  min_subtotal: number
  max_redemptions: number | null
  redemption_count: number
  valid_from: string | null
  valid_until: string | null
  is_active: boolean
}

const EMPTY_FORM = {
  code: '',
  discount_type: 'percent' as 'percent' | 'fixed',
  discount_value: '',
  min_subtotal: '0',
  max_redemptions: '',
  valid_until: '',
}

export default function CouponsPage() {
  const [coupons, setCoupons] = useState<Coupon[]>([])
  const [loadError, setLoadError] = useState<string | null>(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [formError, setFormError] = useState<string | null>(null)
  const [notice, setNotice] = useState<{ kind: 'success' | 'error'; text: string } | null>(null)

  useEffect(() => {
    load()
  }, [])

  async function load() {
    try {
      setCoupons((await ApiClient.get('/coupons')) as Coupon[])
      setLoadError(null)
    } catch (err) {
      setLoadError(errorMessage(err, 'Coupons could not be loaded.'))
    }
  }

  function update(field: keyof typeof EMPTY_FORM, value: string) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  async function createCoupon(event: FormEvent) {
    event.preventDefault()
    setFormError(null)
    const value = Number(form.discount_value)
    if (!(value > 0)) {
      setFormError('The discount must be greater than zero.')
      return
    }
    try {
      const created = (await ApiClient.post('/coupons', {
        code: form.code.trim(),
        discount_type: form.discount_type,
        discount_value: value,
        min_subtotal: Number(form.min_subtotal || '0'),
        max_redemptions: form.max_redemptions.trim() ? Number(form.max_redemptions) : null,
        valid_until: form.valid_until ? new Date(form.valid_until).toISOString() : null,
      })) as Coupon
      setForm(EMPTY_FORM)
      setNotice({ kind: 'success', text: `Coupon ${created.code} created.` })
      await load()
    } catch (err) {
      setFormError(errorMessage(err, 'The coupon could not be created.'))
    }
  }

  async function setActive(coupon: Coupon, isActive: boolean) {
    try {
      await ApiClient.patch(`/coupons/${coupon.id}`, { is_active: isActive })
      setNotice({ kind: 'success', text: `${coupon.code} ${isActive ? 'enabled' : 'disabled'}.` })
      await load()
    } catch (err) {
      setNotice({ kind: 'error', text: errorMessage(err, 'The coupon could not be updated.') })
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Discount codes</h1>

      {notice && (
        <p role={notice.kind === 'error' ? 'alert' : 'status'} className={notice.kind === 'error' ? 'text-red-700' : 'text-green-700'}>
          {notice.text}
        </p>
      )}
      {loadError && <p role="alert" className="text-red-700">{loadError}</p>}

      <section aria-label="Create coupon" className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">New discount code</h2>
        <form onSubmit={createCoupon} className="grid gap-4 md:grid-cols-3">
          <label className="flex flex-col text-sm text-gray-700">
            Code
            <input className="mt-1 rounded border border-gray-300 px-3 py-2" value={form.code} onChange={(e) => update('code', e.target.value)} required minLength={3} maxLength={50} />
          </label>
          <label className="flex flex-col text-sm text-gray-700">
            Type
            <select className="mt-1 rounded border border-gray-300 px-3 py-2" value={form.discount_type} onChange={(e) => update('discount_type', e.target.value)}>
              <option value="percent">Percentage off</option>
              <option value="fixed">Fixed amount off</option>
            </select>
          </label>
          <label className="flex flex-col text-sm text-gray-700">
            Discount value
            <input className="mt-1 rounded border border-gray-300 px-3 py-2" inputMode="decimal" value={form.discount_value} onChange={(e) => update('discount_value', e.target.value)} required />
          </label>
          <label className="flex flex-col text-sm text-gray-700">
            Minimum subtotal
            <input className="mt-1 rounded border border-gray-300 px-3 py-2" inputMode="decimal" value={form.min_subtotal} onChange={(e) => update('min_subtotal', e.target.value)} />
          </label>
          <label className="flex flex-col text-sm text-gray-700">
            Maximum uses (blank for unlimited)
            <input className="mt-1 rounded border border-gray-300 px-3 py-2" inputMode="numeric" value={form.max_redemptions} onChange={(e) => update('max_redemptions', e.target.value)} />
          </label>
          <label className="flex flex-col text-sm text-gray-700">
            Valid until (optional)
            <input type="datetime-local" className="mt-1 rounded border border-gray-300 px-3 py-2" value={form.valid_until} onChange={(e) => update('valid_until', e.target.value)} />
          </label>
          <div>
            <button type="submit" className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">Create code</button>
          </div>
          {formError && <p role="alert" className="md:col-span-3 text-sm text-red-700">{formError}</p>}
        </form>
      </section>

      <section aria-label="Existing coupons" className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Existing codes</h2>
        {coupons.length === 0 ? (
          <p className="text-gray-600">No discount codes yet.</p>
        ) : (
          <table className="min-w-full text-sm">
            <thead className="text-left text-gray-600">
              <tr>
                <th className="py-2">Code</th>
                <th className="py-2">Discount</th>
                <th className="py-2">Used</th>
                <th className="py-2">Valid until</th>
                <th className="py-2">Status</th>
                <th className="py-2" />
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {coupons.map((coupon) => (
                <tr key={coupon.id}>
                  <td className="py-2 font-medium text-gray-900">{coupon.code}</td>
                  <td className="py-2">
                    {coupon.discount_type === 'percent' ? `${coupon.discount_value}%` : `${coupon.discount_value} off`}
                    {coupon.min_subtotal > 0 ? ` (min ${coupon.min_subtotal})` : ''}
                  </td>
                  <td className="py-2">
                    {coupon.redemption_count}
                    {coupon.max_redemptions !== null ? ` / ${coupon.max_redemptions}` : ''}
                  </td>
                  <td className="py-2">{coupon.valid_until ? new Date(coupon.valid_until).toLocaleString() : 'No end date'}</td>
                  <td className="py-2">{coupon.is_active ? 'Active' : 'Disabled'}</td>
                  <td className="py-2 text-right">
                    <button
                      type="button"
                      className="text-blue-700 underline"
                      onClick={() => setActive(coupon, !coupon.is_active)}
                    >
                      {coupon.is_active ? 'Disable' : 'Enable'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  )
}
