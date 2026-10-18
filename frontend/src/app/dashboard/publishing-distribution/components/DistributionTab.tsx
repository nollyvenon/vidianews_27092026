import React, { FormEvent, useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { CheckCircle2 } from 'lucide-react';
import { ApiClient } from '@/lib/api-client';
import { errorMessage } from '@/lib/api-error';

interface DistributionChannel {
  id: number;
  type: string;
  display_name: string;
  success_rate: number;
  priority: number;
}

interface SyndicationPartner {
  id: number;
  partner_name: string;
  partner_type: string;
  articles_syndicated: number;
  reach: number;
}

const PARTNER_TYPES = ['news_agency', 'platform', 'blog_network'];

export default function DistributionTab() {
  const [channels, setChannels] = useState<DistributionChannel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [partners, setPartners] = useState<SyndicationPartner[] | null>(null);
  const [partnersError, setPartnersError] = useState<string | null>(null);
  const [partnerName, setPartnerName] = useState('');
  const [partnerType, setPartnerType] = useState(PARTNER_TYPES[0]);
  const [endpoint, setEndpoint] = useState('');

  const loadPartners = () =>
    ApiClient.get('/distribution/syndication-profiles')
      .then((data: SyndicationPartner[]) => {
        setPartners(Array.isArray(data) ? data : []);
        setPartnersError(null);
      })
      .catch((err) => setPartnersError(errorMessage(err, 'Syndication partners could not be loaded.')));

  useEffect(() => {
    let active = true;
    ApiClient.get('/distribution/channels')
      .then((data: DistributionChannel[]) => {
        if (active) setChannels(Array.isArray(data) ? data : []);
      })
      .catch((err) => {
        if (active) setError(errorMessage(err, 'Distribution channels could not be loaded.'));
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    loadPartners();
    return () => {
      active = false;
    };
  }, []);

  const addPartner = async (event: FormEvent) => {
    event.preventDefault();
    setPartnersError(null);
    try {
      await ApiClient.post('/distribution/syndication-profiles', {
        partner_name: partnerName.trim(),
        partner_type: partnerType,
        api_endpoint: endpoint.trim() || null,
      });
      setPartnerName('');
      setEndpoint('');
      await loadPartners();
    } catch (err) {
      setPartnersError(errorMessage(err, 'The partner could not be added.'));
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Distribution Channels</CardTitle>
          <CardDescription>Active channels for your organization, by priority</CardDescription>
        </CardHeader>
        <CardContent>
          {error && <p role="alert" className="mb-3 text-sm text-red-700">{error}</p>}
          {loading ? (
            <p className="text-sm text-gray-500">Loading channels…</p>
          ) : channels.length === 0 ? (
            <p className="text-sm text-gray-500">No active distribution channels yet.</p>
          ) : (
            <div className="space-y-3">
              {channels.map((channel) => (
                <div key={channel.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h4 className="font-medium">{channel.display_name}</h4>
                    <p className="text-sm text-gray-600">Type: {channel.type} · Priority {channel.priority}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-green-600" />
                    <Badge>{channel.success_rate.toFixed(1)}% success</Badge>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Syndication Partnerships</CardTitle>
          <CardDescription>Partners your content is syndicated to, with the articles and reach they produced</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {partnersError && <p role="alert" className="text-sm text-red-700">{partnersError}</p>}
          {partners === null ? (
            <p className="text-sm text-gray-500">Loading partners…</p>
          ) : partners.length === 0 ? (
            <p className="text-sm text-gray-500">No syndication partners yet.</p>
          ) : (
            <div className="space-y-3">
              {partners.map((partner) => (
                <div key={partner.id} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <div>
                    <p className="font-medium text-sm">{partner.partner_name}</p>
                    <p className="text-xs text-gray-600">{partner.articles_syndicated} articles syndicated · {partner.partner_type}</p>
                  </div>
                  <Badge variant="outline">{partner.reach.toLocaleString()} reach</Badge>
                </div>
              ))}
            </div>
          )}
          <form onSubmit={addPartner} className="flex flex-wrap gap-2 items-end">
            <input className="border rounded px-2 py-1" placeholder="Partner name" value={partnerName} onChange={(e) => setPartnerName(e.target.value)} required />
            <select aria-label="Partner type" className="border rounded px-2 py-1" value={partnerType} onChange={(e) => setPartnerType(e.target.value)}>
              {PARTNER_TYPES.map((type) => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
            <input className="border rounded px-2 py-1" placeholder="API endpoint (optional)" value={endpoint} onChange={(e) => setEndpoint(e.target.value)} />
            <Button type="submit" variant="outline" disabled={!partnerName.trim()}>Add partner</Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
