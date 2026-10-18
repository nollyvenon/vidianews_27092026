'use client'

import { FormEvent, useEffect, useState } from 'react'
import { ApiClient } from '@/lib/api-client'
import { errorMessage } from '@/lib/api-error'

interface Product {
  id: number
  name: string
  price: number
  category: string | null
  stock_quantity: number
  average_rating: number
  review_count: number
}

/** The product catalogue, with search and a category filter. */
export default function MarketplacePage() {
  const [products, setProducts] = useState<Product[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState('')

  const load = (path: string) =>
    ApiClient.get(path)
      .then((data: Product[]) => {
        setProducts(Array.isArray(data) ? data : []);
        setError(null);
      })
      .catch((err) => setError(errorMessage(err, 'Products could not be loaded.')));

  useEffect(() => {
    load(category ? `/products?category=${encodeURIComponent(category)}` : '/products');
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [category]);

  const search = (event: FormEvent) => {
    event.preventDefault();
    if (!query.trim()) {
      load(category ? `/products?category=${encodeURIComponent(category)}` : '/products');
      return;
    }
    load(`/products/search?q=${encodeURIComponent(query.trim())}`);
  };

  const categories = Array.from(new Set((products ?? []).map((product) => product.category).filter(Boolean) as string[])).sort();

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Marketplace</h1>
      {error && <p role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3">{error}</p>}

      <div className="flex flex-wrap gap-3 items-end">
        <form onSubmit={search} className="flex gap-2">
          <input className="border rounded px-3 py-2" placeholder="Search products" value={query} onChange={(e) => setQuery(e.target.value)} />
          <button type="submit" className="px-3 py-2 border border-blue-600 text-blue-600 rounded">Search</button>
        </form>
        <label className="text-sm">
          <span className="block text-xs text-gray-600">Category</span>
          <select className="border rounded px-2 py-2" value={category} onChange={(e) => setCategory(e.target.value)}>
            <option value="">All categories</option>
            {categories.map((item) => (
              <option key={item} value={item}>{item}</option>
            ))}
          </select>
        </label>
      </div>

      {products === null && !error ? (
        <p className="text-gray-500">Loading products…</p>
      ) : products && products.length === 0 ? (
        <p className="text-gray-500">No products match.</p>
      ) : products ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {products.map((product) => (
            <div key={product.id} className="bg-white rounded-lg shadow p-4 space-y-1">
              <p className="font-semibold">{product.name}</p>
              <p className="text-sm text-gray-600">{product.category ?? 'Uncategorised'}</p>
              <p className="text-lg font-bold">${Number(product.price).toFixed(2)}</p>
              <p className="text-sm text-gray-600">
                {product.average_rating.toFixed(1)} ★ ({product.review_count} reviews) · {product.stock_quantity > 0 ? `${product.stock_quantity} in stock` : 'Out of stock'}
              </p>
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}
