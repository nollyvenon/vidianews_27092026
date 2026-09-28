'use client';

import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

interface MembershipPlan {
  id: number;
  name: string;
  tier: string;
  price: number;
  billing_cycle: string;
  max_courses: number;
  features: Record<string, boolean>;
  is_active: boolean;
}

interface Subscription {
  id: number;
  status: string;
  start_date: string;
  renewal_date: string;
  membership_type: MembershipPlan;
}

export default function MembershipsPage() {
  const [plans, setPlans] = useState<MembershipPlan[]>([]);
  const [activeSubscription, setActiveSubscription] = useState<Subscription | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch('/api/v1/membership-types').then(r => r.json()),
      fetch('/api/v1/subscriptions/me/active').then(r => r.json().catch(() => null))
    ]).then(([plansData, subscriptionData]) => {
      setPlans(plansData);
      setActiveSubscription(subscriptionData);
      setLoading(false);
    });
  }, []);

  const handleSubscribe = async (planId: number) => {
    try {
      const response = await fetch('/api/v1/subscriptions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ membership_type_id: planId })
      });
      const newSubscription = await response.json();
      setActiveSubscription(newSubscription);
    } catch (error) {
      console.error('Subscription failed:', error);
    }
  };

  const handleCancel = async () => {
    if (activeSubscription) {
      try {
        await fetch(`/api/v1/subscriptions/${activeSubscription.id}/cancel`, { method: 'POST' });
        setActiveSubscription(null);
      } catch (error) {
        console.error('Cancellation failed:', error);
      }
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Membership Plans</h1>

      {activeSubscription && (
        <Card className="mb-6 p-4 bg-blue-50">
          <h2 className="text-xl font-semibold mb-2">Active Subscription</h2>
          <p className="mb-2">Plan: {activeSubscription.membership_type.name}</p>
          <p className="mb-2">Status: {activeSubscription.status}</p>
          <p className="mb-4">Renewal Date: {new Date(activeSubscription.renewal_date).toLocaleDateString()}</p>
          <Button onClick={handleCancel} variant="destructive">Cancel Subscription</Button>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {plans.map(plan => (
          <Card key={plan.id} className="p-4">
            <h3 className="text-lg font-bold mb-2">{plan.name}</h3>
            <p className="text-2xl font-bold mb-2">${plan.price.toFixed(2)}</p>
            <p className="text-sm text-gray-600 mb-3">per {plan.billing_cycle}</p>
            <ul className="text-sm mb-4">
              {Object.entries(plan.features).map(([feature, enabled]) => (
                <li key={feature} className={enabled ? 'text-green-600' : 'text-gray-400'}>
                  {feature}: {enabled ? '✓' : '✗'}
                </li>
              ))}
            </ul>
            <p className="text-sm mb-4">Max Courses: {plan.max_courses === -1 ? 'Unlimited' : plan.max_courses}</p>
            <Button
              onClick={() => handleSubscribe(plan.id)}
              disabled={activeSubscription?.membership_type.id === plan.id}
              className="w-full"
            >
              {activeSubscription?.membership_type.id === plan.id ? 'Current Plan' : 'Subscribe'}
            </Button>
          </Card>
        ))}
      </div>
    </div>
  );
}
