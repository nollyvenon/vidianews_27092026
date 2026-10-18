'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

export interface ShippingAddress {
  id: number
  first_name: string
  last_name: string
  street_address: string
  city: string
  state: string | null
  postal_code: string
  country: string
  phone: string | null
  is_default: boolean
}

const EMPTY_FORM = {
  first_name: '',
  last_name: '',
  street_address: '',
  city: '',
  state: '',
  postal_code: '',
  country: '',
  phone: '',
  is_default: false,
}

export default function ShippingAddressesPage() {
  const [addresses, setAddresses] = useState<ShippingAddress[]>([])
  const [loadError, setLoadError] = useState<string | null>(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [formError, setFormError] = useState<string | null>(null)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    load()
  }, [])

  async function load() {
    try {
      setAddresses((await ApiClient.get('/shipping-addresses')) as ShippingAddress[])
      setLoadError(null)
    } catch (err) {
      setLoadError(errorMessage(err, 'Your addresses could not be loaded.'))
    }
  }

  function update(field: keyof typeof EMPTY_FORM, value: string | boolean) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  async function save(event: FormEvent) {
    event.preventDefault()
    setFormError(null)
    setSaved(false)
    try {
      await ApiClient.post('/shipping-addresses', {
        ...form,
        state: form.state.trim() || null,
        phone: form.phone.trim() || null,
      })
      setForm(EMPTY_FORM)
      setSaved(true)
      await load()
    } catch (err) {
      setFormError(errorMessage(err, 'The address could not be saved.'))
    }
  }

  const fields: { key: keyof typeof EMPTY_FORM; label: string; required?: boolean }[] = [
    { key: 'first_name', label: 'First name', required: true },
    { key: 'last_name', label: 'Last name', required: true },
    { key: 'street_address', label: 'Street address', required: true },
    { key: 'city', label: 'City', required: true },
    { key: 'state', label: 'State / region' },
    { key: 'postal_code', label: 'Postal code', required: true },
    { key: 'country', label: 'Country', required: true },
    { key: 'phone', label: 'Phone' },
  ]

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Shipping addresses</h1>

      {loadError && <p role="alert" className="text-red-700">{loadError}</p>}

      <section aria-label="Saved addresses" className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Saved addresses</h2>
        {addresses.length === 0 ? (
          <p className="text-gray-600">You have no saved addresses.</p>
        ) : (
          <ul className="space-y-3">
            {addresses.map((address) => (
              <li key={address.id} className="rounded border border-gray-200 p-4">
                <p className="font-medium text-gray-900">
                  {address.first_name} {address.last_name}
                  {address.is_default && <span className="ml-2 text-xs text-blue-700">Default</span>}
                </p>
                <p className="text-gray-700">
                  {address.street_address}, {address.city}
                  {address.state ? `, ${address.state}` : ''} {address.postal_code}, {address.country}
                </p>
                {address.phone && <p className="text-gray-600 text-sm">{address.phone}</p>}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section aria-label="Add address" className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Add an address</h2>
        <form onSubmit={save} className="grid gap-4 md:grid-cols-2">
          {fields.map((field) => (
            <label key={field.key} className="flex flex-col text-sm text-gray-700">
              {field.label}
              <input
                className="mt-1 rounded border border-gray-300 px-3 py-2"
                value={form[field.key] as string}
                onChange={(e) => update(field.key, e.target.value)}
                required={field.required}
              />
            </label>
          ))}
          <label className="flex items-center gap-2 text-sm text-gray-700">
            <input type="checkbox" checked={form.is_default} onChange={(e) => update('is_default', e.target.checked)} />
            Use as my default address
          </label>
          <div>
            <button type="submit" className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">
              Save address
            </button>
          </div>
          {formError && <p role="alert" className="md:col-span-2 text-sm text-red-700">{formError}</p>}
          {saved && <p role="status" className="md:col-span-2 text-sm text-green-700">Address saved.</p>}
        </form>
      </section>
    </div>
  )
}
