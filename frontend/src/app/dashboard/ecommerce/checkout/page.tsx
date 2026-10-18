"use client";

import React, { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { loadStripe, type Stripe } from "@stripe/stripe-js";
import { CardElement, Elements, useElements, useStripe } from "@stripe/react-stripe-js";
import { errorMessage } from "@/lib/api-error";

let stripeLoader: Promise<Stripe | null> | null = null;

/**
 * Stripe.js instance for NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY, or null when no key is configured.
 * Card details are tokenised by Stripe.js in the browser; this page never sees the raw card number.
 */
function getStripePromise(): Promise<Stripe | null> | null {
  const publishableKey = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY;
  if (!publishableKey) return null;
  if (!stripeLoader) stripeLoader = loadStripe(publishableKey);
  return stripeLoader;
}

type Address = { street: string; city: string; state: string; zip: string; country: string };

const EMPTY_ADDRESS: Address = { street: "", city: "", state: "", zip: "", country: "" };

const CARD_STYLE = {
  style: { base: { fontSize: "16px", color: "#111827", "::placeholder": { color: "#9ca3af" } } },
};

function CheckoutForm({ configured }: { configured: boolean }) {
  const router = useRouter();
  const stripe = useStripe();
  const elements = useElements();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [checkoutData, setCheckoutData] = useState({
    billing_address: { ...EMPTY_ADDRESS },
    shipping_address: { ...EMPTY_ADDRESS },
    email: "",
    phone: "",
    shipping_method: "standard",
  });

  const handleCheckoutChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (name.includes(".")) {
      const [section, field] = name.split(".") as ["billing_address" | "shipping_address", keyof Address];
      setCheckoutData((prev) => ({
        ...prev,
        [section]: { ...prev[section], [field]: value },
      }));
    } else {
      setCheckoutData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!stripe || !elements) {
      setError("Card payments are not ready yet. Please try again in a moment.");
      return;
    }

    setLoading(true);
    try {
      const checkout = (await axios.post("/api/v1/checkout", checkoutData)).data;

      const card = elements.getElement(CardElement);
      if (!card) {
        setError("Enter your card details to continue.");
        return;
      }
      const billing = checkoutData.billing_address;
      const { paymentMethod, error: stripeError } = await stripe.createPaymentMethod({
        type: "card",
        card,
        billing_details: {
          email: checkoutData.email,
          address: {
            line1: billing.street,
            city: billing.city,
            state: billing.state,
            postal_code: billing.zip,
            country: billing.country,
          },
        },
      });
      if (stripeError || !paymentMethod) {
        setError(stripeError?.message ?? "Your card could not be verified.");
        return;
      }

      const payment = (
        await axios.post(`/api/v1/checkout/${checkout.id}/payment`, {
          payment_method: "stripe",
          amount: checkout.total,
          card_token: paymentMethod.id,
        })
      ).data;
      router.push(`/dashboard/ecommerce/order-confirmation/${payment.order_id}`);
    } catch (err) {
      setError(errorMessage(err, "Checkout could not be completed."));
    } finally {
      setLoading(false);
    }
  };

  const addressFields = (section: "billing_address" | "shipping_address") => (
    <div className="space-y-4">
      {(
        [
          ["street", "Street"],
          ["city", "City"],
          ["state", "State"],
          ["zip", "ZIP Code"],
          ["country", "Country"],
        ] as const
      ).map(([field, label]) => (
        <input
          key={field}
          type="text"
          name={`${section}.${field}`}
          placeholder={label}
          value={checkoutData[section][field]}
          onChange={handleCheckoutChange}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg"
          required
        />
      ))}
    </div>
  );

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Checkout</h1>

      {!configured && (
        <div role="alert" className="bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-lg p-4">
          Card payments are not configured. Set NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY for this app and restart it.
        </div>
      )}
      {error && (
        <div role="alert" className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Contact Information</h3>
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
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Billing Address</h3>
            {addressFields("billing_address")}
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Shipping Address</h3>
            {addressFields("shipping_address")}
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Shipping Method</h3>
            <div className="space-y-2">
              {[
                ["standard", "Standard (5-7 days) - $5"],
                ["express", "Express (2-3 days) - $15"],
                ["overnight", "Overnight - $25"],
              ].map(([value, label]) => (
                <label key={value} className="flex items-center">
                  <input
                    type="radio"
                    name="shipping_method"
                    value={value}
                    checked={checkoutData.shipping_method === value}
                    onChange={handleCheckoutChange}
                  />
                  <span className="ml-2">{label}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Card Details</h3>
            <div className="border border-gray-300 rounded-lg px-4 py-3">
              <CardElement options={CARD_STYLE} />
            </div>
            <p className="text-xs text-gray-500 mt-2">Card details are sent directly to Stripe and never stored here.</p>
          </div>

          <button
            type="submit"
            disabled={loading || !stripe || !configured}
            className="w-full px-4 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Processing..." : "Complete Purchase"}
          </button>
        </div>
      </form>
    </div>
  );
}

export default function CheckoutPage() {
  // Elements with a null Stripe instance keeps the hooks valid; the form then shows the
  // configuration notice and disables submission.
  const stripePromise = getStripePromise();
  return (
    <Elements stripe={stripePromise}>
      <CheckoutForm configured={stripePromise !== null} />
    </Elements>
  );
}
