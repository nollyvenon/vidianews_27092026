import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle2, AlertCircle } from 'lucide-react';

export default function DistributionTab() {
  const channels = [
    { name: 'Website', status: 'active', reach: '125K', rate: '89.5%' },
    { name: 'Email', status: 'active', reach: '89K', rate: '67.2%' },
    { name: 'Twitter', status: 'active', reach: '245K', rate: '4.2%' },
    { name: 'LinkedIn', status: 'active', reach: '156K', rate: '6.8%' },
    { name: 'RSS', status: 'active', reach: '34K', rate: '12.1%' },
  ];

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Distribution Channels</CardTitle>
          <CardDescription>Performance across all distribution channels</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {channels.map((channel) => (
              <div key={channel.name} className="flex items-center justify-between p-4 border rounded-lg">
                <div>
                  <h4 className="font-medium">{channel.name}</h4>
                  <p className="text-sm text-gray-600">Reach: {channel.reach}</p>
                </div>
                <div className="text-right">
                  <div className="flex items-center gap-2 mb-1">
                    <CheckCircle2 className="h-4 w-4 text-green-600" />
                    <Badge>{channel.rate} engagement</Badge>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Syndication Partnerships</CardTitle>
          <CardDescription>Active content syndication agreements</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {[
              { partner: 'News Agency Pro', articles: 156, reach: '1.2M' },
              { partner: 'Tech Blog Network', articles: 89, reach: '450K' },
              { partner: 'Industry Digest', articles: 42, reach: '320K' },
            ].map((partner, idx) => (
              <div key={idx} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <div>
                  <p className="font-medium text-sm">{partner.partner}</p>
                  <p className="text-xs text-gray-600">{partner.articles} articles syndicated</p>
                </div>
                <Badge variant="outline">{partner.reach} reach</Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
