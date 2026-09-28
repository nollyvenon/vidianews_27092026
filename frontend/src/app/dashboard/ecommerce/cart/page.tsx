"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import Link from "next/link";

interface CartItem {
  id: number;
  product_id: number;
  quantity: number;
  unit_price: number;
  line_total: number;
}

interface Cart {
  id: number;
  subtotal: number;
  tax: number;
  shipping: number;
  discount: number;
  total: number;
  item_count: number;
  items: CartItem[];
}

export default function CartPage() {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCart();
  }, []);

  const fetchCart = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/api/v1/cart");
      setCart(response.data);
    } catch (error) {
      console.error("Error fetching cart:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateQuantity = async (itemId: number, quantity: number) => {
    try {
      await axios.put(`/api/v1/cart/items/${itemId}`, { quantity });
      fetchCart();
    } catch (error) {
      console.error("Error updating quantity:", error);
    }
  };

  const handleRemoveItem = async (itemId: number) => {
    try {
      await axios.delete(`/api/v1/cart/items/${itemId}`);
      fetchCart();
    } catch (error) {
      console.error("Error removing item:", error);
    }
  };

  const handleClearCart = async () => {
    try {
      await axios.delete("/api/v1/cart");
      setCart(null);
    } catch (error) {
      console.error("Error clearing cart:", error);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  if (!cart || cart.item_count === 0) {
    return (
      <div className="space-y-6">
        <h1 className="text-3xl font-bold text-gray-900">Shopping Cart</h1>
        <div className="bg-white rounded-lg shadow p-8 text-center">
          <p className="text-gray-600 mb-4">Your cart is empty</p>
          <Link
            href="/dashboard/ecommerce/products"
            className="inline-block px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Continue Shopping
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Shopping Cart</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-gray-900">Product</th>
                  <th className="px-6 py-3 text-left text-gray-900">Price</th>
                  <th className="px-6 py-3 text-left text-gray-900">Quantity</th>
                  <th className="px-6 py-3 text-left text-gray-900">Total</th>
                  <th className="px-6 py-3 text-left text-gray-900">Action</th>
                </tr>
              </thead>
              <tbody>
                {cart.items.map((item) => (
                  <tr key={item.id} className="border-b">
                    <td className="px-6 py-4">Product {item.product_id}</td>
                    <td className="px-6 py-4">${item.unit_price}</td>
                    <td className="px-6 py-4">
                      <input
                        type="number"
                        min="1"
                        value={item.quantity}
                        onChange={(e) =>
                          handleUpdateQuantity(item.id, parseInt(e.target.value))
                        }
                        className="w-16 px-2 py-1 border border-gray-300 rounded"
                      />
                    </td>
                    <td className="px-6 py-4">${item.line_total}</td>
                    <td className="px-6 py-4">
                      <button
                        onClick={() => handleRemoveItem(item.id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        Remove
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 h-fit">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Order Summary
          </h3>
          <div className="space-y-2 mb-4 pb-4 border-b">
            <div className="flex justify-between">
              <span className="text-gray-600">Subtotal</span>
              <span className="font-semibold">${cart.subtotal}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Tax</span>
              <span className="font-semibold">${cart.tax}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Shipping</span>
              <span className="font-semibold">${cart.shipping}</span>
            </div>
            {cart.discount > 0 && (
              <div className="flex justify-between">
                <span className="text-gray-600">Discount</span>
                <span className="font-semibold text-green-600">
                  -${cart.discount}
                </span>
              </div>
            )}
          </div>
          <div className="flex justify-between mb-6">
            <span className="text-lg font-bold">Total</span>
            <span className="text-lg font-bold text-blue-600">
              ${cart.total}
            </span>
          </div>
          <Link
            href="/dashboard/ecommerce/checkout"
            className="w-full block text-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 mb-2"
          >
            Proceed to Checkout
          </Link>
          <button
            onClick={handleClearCart}
            className="w-full px-4 py-2 border border-red-600 text-red-600 rounded-lg hover:bg-red-50"
          >
            Clear Cart
          </button>
        </div>
      </div>
    </div>
  );
}
