"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";

export default function CheckoutPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [checkoutData, setCheckoutData] = useState({
    billing_address: {
      street: "",
      city: "",
      state: "",
      zip: "",
      country: "",
    },
    shipping_address: {
      street: "",
      city: "",
      state: "",
      zip: "",
      country: "",
    },
    email: "",
    phone: "",
    shipping_method: "standard",
  });

  const [paymentData, setPaymentData] = useState({
    payment_method: "stripe",
    card_token: "",
  });

  const handleCheckoutChange = (e: any) => {
    const { name, value } = e.target;
    if (name.includes(".")) {
      const [section, field] = name.split(".");
      setCheckoutData((prev) => ({
        ...prev,
        [section]: {
          ...prev[section as keyof typeof checkoutData],
          [field]: value,
        },
      }));
    } else {
      setCheckoutData((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);

      const checkoutResponse = await axios.post(
        "/api/v1/checkout",
        checkoutData
      );
      const checkout = checkoutResponse.data;

      const paymentResponse = await axios.post(
        `/api/v1/checkout/${checkout.id}/payment`,
        {
          ...paymentData,
          amount: checkout.total,
        }
      );

      router.push(`/dashboard/ecommerce/order-confirmation/${checkout.id}`);
    } catch (error) {
      console.error("Error during checkout:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Checkout</h1>

      <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Contact Information
            </h3>
            <div className="space-y-4">
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={checkoutData.email}
                onChange={handleCheckoutChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                required
              />
              <input
                type="tel"
                name="phone"
                placeholder="Phone"
                value={checkoutData.phone}
                onChange={handleCheckoutChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Billing Address
            </h3>
            <div className="space-y-4">
              <input
                type="text"
                name="billing_address.street"
                placeholder="Street"
                value={checkoutData.billing_address.street}
                onChange={handleCheckoutChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                required
              />
              <input
                type="text"
                name="billing_address.city"
                placeholder="City"
                value={checkoutData.billing_address.city}
                onChange={handleCheckoutChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                required
              />
              <input
                type="text"
                name="billing_address.state"
                placeholder="State"
                value={checkoutData.billing_address.state}
                onChange={handleCheckoutChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                required
              />
              <input
                type="text"
                name="billing_address.zip"
                placeholder="ZIP Code"
                value={checkoutData.billing_address.zip}
                onChange={handleCheckoutChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                required
              />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Shipping Address
            </h3>
            <div className="space-y-4">
              <input
                type="text"
                name="shipping_address.street"
                placeholder="Street"
                value={checkoutData.shipping_address.street}
                onChange={handleCheckoutChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                required
              />
              <input
                type="text"
                name="shipping_address.city"
                placeholder="City"
                value={checkoutData.shipping_address.city}
                onChange={handleCheckoutChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                required
              />
              <input
                type="text"
                name="shipping_address.state"
                placeholder="State"
                value={checkoutData.shipping_address.state}
                onChange={handleCheckoutChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                required
              />
              <input
                type="text"
                name="shipping_address.zip"
                placeholder="ZIP Code"
                value={checkoutData.shipping_address.zip}
                onChange={handleCheckoutChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                required
              />
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Shipping Method
            </h3>
            <div className="space-y-2">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="shipping_method"
                  value="standard"
                  checked={checkoutData.shipping_method === "standard"}
                  onChange={handleCheckoutChange}
                />
                <span className="ml-2">Standard (5-7 days) - $5</span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="shipping_method"
                  value="express"
                  checked={checkoutData.shipping_method === "express"}
                  onChange={handleCheckoutChange}
                />
                <span className="ml-2">Express (2-3 days) - $15</span>
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="shipping_method"
                  value="overnight"
                  checked={checkoutData.shipping_method === "overnight"}
                  onChange={handleCheckoutChange}
                />
                <span className="ml-2">Overnight - $25</span>
              </label>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Payment Method
            </h3>
            <div className="space-y-4">
              <input
                type="text"
                name="card_number"
                placeholder="Card Number"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
              <div className="grid grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="MM/YY"
                  className="px-4 py-2 border border-gray-300 rounded-lg"
                />
                <input
                  type="text"
                  placeholder="CVC"
                  className="px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full px-4 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Processing..." : "Complete Purchase"}
          </button>
        </div>
      </form>
    </div>
  );
}
