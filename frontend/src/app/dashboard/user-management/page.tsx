import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, Mail, TrendingUp, Bell, Zap } from 'lucide-react';

export default function UserManagementDashboard() {
  return (
    <div className="space-y-6">
      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Users className="h-4 w-4" />
              Total Subscribers
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">24,500</div>
            <p className="text-xs text-gray-500">+2,300 this month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Mail className="h-4 w-4" />
              Campaigns Sent
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">156</div>
            <p className="text-xs text-gray-500">8 in last 7 days</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm">
              <TrendingUp className="h-4 w-4" />
              Avg Engagement
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">68.5%</div>
            <p className="text-xs text-gray-500">Up 5.2% this week</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Bell className="h-4 w-4" />
              Active Segments
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-gray-500">8 dynamic segments</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-sm">
              <Zap className="h-4 w-4" />
              Churn Risk
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12.3%</div>
            <p className="text-xs text-gray-500">-2.1% improvement</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Subscriber Tiers */}
        <Card>
          <CardHeader>
            <CardTitle>Subscriber Distribution</CardTitle>
            <CardDescription>By subscription tier</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                { tier: 'Free', count: 15200, percent: 62 },
                { tier: 'Premium', count: 7500, percent: 31 },
                { tier: 'Enterprise', count: 1800, percent: 7 },
              ].map((item) => (
                <div key={item.tier} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium">{item.tier}</span>
                    <span className="text-gray-600">{item.count.toLocaleString()}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${item.percent}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Engagement Score Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Engagement Levels</CardTitle>
            <CardDescription>Subscriber segments by engagement</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {[
                { label: 'Highly Engaged', count: 8200, color: 'bg-green-600' },
                { label: 'Engaged', count: 10500, color: 'bg-blue-600' },
                { label: 'Low Engagement', count: 4300, color: 'bg-orange-600' },
                { label: 'Inactive', count: 1500, color: 'bg-red-600' },
              ].map((item) => (
                <div key={item.label} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className={`w-3 h-3 rounded-full ${item.color}`}></div>
                    <span className="text-sm">{item.label}</span>
                  </div>
                  <span className="text-sm font-medium">{item.count}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Campaign Performance */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Campaigns</CardTitle>
          <CardDescription>Email campaign performance</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              { name: 'Weekly Tech Digest', sent: 8500, opens: 5610, clicks: 787, ctr: 9.3 },
              { name: 'New Feature Announcement', sent: 12300, opens: 8610, clicks: 1353, ctr: 11 },
              { name: 'Exclusive Offer - Premium', sent: 7200, opens: 5040, clicks: 705, ctr: 9.8 },
            ].map((campaign) => (
              <div key={campaign.name} className="border rounded-lg p-3">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <p className="font-medium text-sm">{campaign.name}</p>
                    <p className="text-xs text-gray-600">Sent to {campaign.sent.toLocaleString()}</p>
                  </div>
                  <span className="text-sm font-semibold text-green-600">{campaign.ctr}% CTR</span>
                </div>
                <div className="flex gap-4 text-xs">
                  <span className="text-gray-600">Opens: {campaign.opens}</span>
                  <span className="text-gray-600">Clicks: {campaign.clicks}</span>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Churn Risk */}
      <Card>
        <CardHeader>
          <CardTitle>At-Risk Subscribers</CardTitle>
          <CardDescription>Users likely to churn in next 30 days</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {[
              { risk: 'High Risk (>80%)', count: 450, action: 'Urgent outreach' },
              { risk: 'Medium Risk (50-80%)', count: 1200, action: 'Engagement campaign' },
              { risk: 'Low Risk (<50%)', count: 3500, action: 'Monitor' },
            ].map((item) => (
              <div key={item.risk} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <div>
                  <p className="font-medium text-sm">{item.risk}</p>
                  <p className="text-xs text-gray-600">{item.count} subscribers</p>
                </div>
                <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                  {item.action}
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
