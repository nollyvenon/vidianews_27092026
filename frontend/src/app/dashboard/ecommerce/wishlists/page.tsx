'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

export interface Wishlist {
  id: number
  name: string
  description: string | null
  is_public: boolean
  share_token: string
}

export interface WishlistItem {
  id: number
  wishlist_id: number
  product_id: number
  priority: number
  notes: string | null
  added_at: string | null
}

interface ItemView extends WishlistItem {
  productName: string
}

export default function WishlistsPage() {
  const [wishlists, setWishlists] = useState<Wishlist[]>([])
  const [loadError, setLoadError] = useState<string | null>(null)
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const [items, setItems] = useState<ItemView[]>([])
  const [itemsError, setItemsError] = useState<string | null>(null)
  const [notice, setNotice] = useState<{ kind: 'success' | 'error'; text: string } | null>(null)

  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [isPublic, setIsPublic] = useState(false)
  const [createError, setCreateError] = useState<string | null>(null)

  const [productId, setProductId] = useState('')
  const [addError, setAddError] = useState<string | null>(null)

  const selected = wishlists.find((w) => w.id === selectedId) ?? null

  useEffect(() => {
    loadWishlists()
  }, [])

  useEffect(() => {
    if (selectedId !== null) loadItems(selectedId)
    else setItems([])
  }, [selectedId])

  async function loadWishlists() {
    try {
      const data = (await ApiClient.get('/wishlists')) as Wishlist[]
      setWishlists(data)
      setLoadError(null)
      setSelectedId((current) => current ?? (data[0]?.id ?? null))
    } catch (err) {
      setLoadError(errorMessage(err, 'Your wishlists could not be loaded.'))
    }
  }

  async function loadItems(wishlistId: number) {
    try {
      const rows = (await ApiClient.get(`/wishlists/${wishlistId}/items`)) as WishlistItem[]
      const named = await Promise.all(
        rows.map(async (row): Promise<ItemView> => {
          try {
            const product = (await ApiClient.get(`/products/${row.product_id}`)) as { name?: string }
            return { ...row, productName: product.name ?? `Product #${row.product_id}` }
          } catch {
            return { ...row, productName: `Product #${row.product_id}` }
          }
        }),
      )
      setItems(named)
      setItemsError(null)
    } catch (err) {
      setItemsError(errorMessage(err, 'The items could not be loaded.'))
    }
  }

  async function createWishlist(event: FormEvent) {
    event.preventDefault()
    setCreateError(null)
    try {
      const created = (await ApiClient.post('/wishlists', {
        name: name.trim(),
        description: description.trim() || null,
        is_public: isPublic,
      })) as Wishlist
      setName('')
      setDescription('')
      setIsPublic(false)
      setWishlists((current) => [...current, created])
      setSelectedId(created.id)
      setNotice({ kind: 'success', text: `Wishlist "${created.name}" created.` })
    } catch (err) {
      setCreateError(errorMessage(err, 'The wishlist could not be created.'))
    }
  }

  async function addProduct(event: FormEvent) {
    event.preventDefault()
    if (selectedId === null) return
    const id = Number(productId)
    if (!Number.isInteger(id) || id <= 0) {
      setAddError('Enter a valid product number.')
      return
    }
    setAddError(null)
    try {
      await ApiClient.post(`/wishlists/${selectedId}/items/${id}`, {})
      setProductId('')
      setNotice({ kind: 'success', text: 'Product added to the wishlist.' })
      await loadItems(selectedId)
    } catch (err) {
      setAddError(errorMessage(err, 'The product could not be added.'))
    }
  }

  async function removeItem(item: ItemView) {
    try {
      await ApiClient.delete(`/wishlist-items/${item.id}`)
      setItems((current) => current.filter((row) => row.id !== item.id))
      setNotice({ kind: 'success', text: `${item.productName} removed.` })
    } catch (err) {
      setNotice({ kind: 'error', text: errorMessage(err, 'The item could not be removed.') })
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Wishlists</h1>

      {notice && (
        <p role={notice.kind === 'error' ? 'alert' : 'status'} className={notice.kind === 'error' ? 'text-red-700' : 'text-green-700'}>
          {notice.text}
        </p>
      )}
      {loadError && <p role="alert" className="text-red-700">{loadError}</p>}

      <section aria-label="Create wishlist" className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">New wishlist</h2>
        <form onSubmit={createWishlist} className="grid gap-4 md:grid-cols-2">
          <label className="flex flex-col text-sm text-gray-700">
            Name
            <input
              className="mt-1 rounded border border-gray-300 px-3 py-2"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              maxLength={255}
            />
          </label>
          <label className="flex flex-col text-sm text-gray-700">
            Description
            <input
              className="mt-1 rounded border border-gray-300 px-3 py-2"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </label>
          <label className="flex items-center gap-2 text-sm text-gray-700">
            <input type="checkbox" checked={isPublic} onChange={(e) => setIsPublic(e.target.checked)} />
            Share this wishlist publicly
          </label>
          <div>
            <button type="submit" className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">
              Create wishlist
            </button>
          </div>
          {createError && <p role="alert" className="md:col-span-2 text-sm text-red-700">{createError}</p>}
        </form>
      </section>

      <section aria-label="Your wishlists" className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Your wishlists</h2>
        {wishlists.length === 0 ? (
          <p className="text-gray-600">You have no wishlists yet.</p>
        ) : (
          <ul className="flex flex-wrap gap-2">
            {wishlists.map((wishlist) => (
              <li key={wishlist.id}>
                <button
                  type="button"
                  aria-pressed={wishlist.id === selectedId}
                  onClick={() => setSelectedId(wishlist.id)}
                  className={`px-3 py-1 rounded border text-sm ${
                    wishlist.id === selectedId ? 'bg-blue-600 text-white border-blue-600' : 'border-gray-300 text-gray-700'
                  }`}
                >
                  {wishlist.name}
                  {wishlist.is_public ? ' (public)' : ''}
                </button>
              </li>
            ))}
          </ul>
        )}
      </section>

      {selected && (
        <section aria-label="Selected wishlist" className="bg-white rounded-lg shadow p-6 space-y-4">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">{selected.name}</h2>
            {selected.description && <p className="text-gray-600">{selected.description}</p>}
            {selected.is_public && (
              <p className="mt-2 text-sm text-gray-700">
                Share token: <code className="break-all">{selected.share_token}</code>
              </p>
            )}
          </div>

          <form onSubmit={addProduct} className="flex flex-wrap items-end gap-3">
            <label className="flex flex-col text-sm text-gray-700">
              Product number
              <input
                className="mt-1 rounded border border-gray-300 px-3 py-2"
                inputMode="numeric"
                value={productId}
                onChange={(e) => setProductId(e.target.value)}
              />
            </label>
            <button type="submit" className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">
              Add product
            </button>
            {addError && <p role="alert" className="w-full text-sm text-red-700">{addError}</p>}
          </form>

          {itemsError && <p role="alert" className="text-red-700">{itemsError}</p>}
          {items.length === 0 && !itemsError ? (
            <p className="text-gray-600">No products in this wishlist yet.</p>
          ) : (
            <ul className="divide-y divide-gray-200">
              {items.map((item) => (
                <li key={item.id} className="flex items-center justify-between py-3">
                  <span className="text-gray-900">{item.productName}</span>
                  <button
                    type="button"
                    onClick={() => removeItem(item)}
                    className="text-sm text-red-700 underline"
                    aria-label={`Remove ${item.productName}`}
                  >
                    Remove
                  </button>
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
    </div>
  )
}
