import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { AlertCircle, CheckCircle2 } from 'lucide-react';

export default function ABTestingTab() {
  const tests = [
    {
      id: 1,
      name: 'Email Subject Line Test',
      status: 'running',
      variantA: { name: 'Current', ctr: 4.2, conversions: 128 },
      variantB: { name: 'Test', ctr: 5.8, conversions: 156 },
      winner: null,
      progress: 65,
    },
    {
      id: 2,
      name: 'CTA Button Color Test',
      status: 'completed',
      variantA: { name: 'Blue', ctr: 3.1, conversions: 95 },
      variantB: { name: 'Green', ctr: 4.5, conversions: 142 },
      winner: 'B',
      progress: 100,
    },
  ];

  return (
    <div className="space-y-6">
      {tests.map((test) => (
        <Card key={test.id}>
          <CardHeader>
            <div className="flex justify-between items-start">
              <div>
                <CardTitle>{test.name}</CardTitle>
                <CardDescription>Variant comparison and analysis</CardDescription>
              </div>
              <Badge variant={test.status === 'running' ? 'default' : 'outline'}>
                {test.status}
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm font-medium">Progress</span>
                <span className="text-sm text-gray-600">{test.progress}%</span>
              </div>
              <Progress value={test.progress} className="h-2" />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-medium text-sm mb-2">{test.variantA.name}</h4>
                <div className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">CTR</span>
                    <span className="font-semibold">{test.variantA.ctr}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Conversions</span>
                    <span className="font-semibold">{test.variantA.conversions}</span>
                  </div>
                </div>
              </div>

              <div className="border rounded-lg p-4 border-green-200 bg-green-50">
                <h4 className="font-medium text-sm mb-2">{test.variantB.name}</h4>
                <div className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">CTR</span>
                    <span className="font-semibold">{test.variantB.ctr}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Conversions</span>
                    <span className="font-semibold">{test.variantB.conversions}</span>
                  </div>
                </div>
              </div>
            </div>

            {test.status === 'completed' && test.winner && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-3 flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-green-600" />
                <span className="text-sm">
                  Variant <strong>{test.winner}</strong> is the winner! {test.variantB.ctr}% CTR vs {test.variantA.ctr}%
                </span>
              </div>
            )}

            <Button className="w-full">{test.status === 'running' ? 'View Details' : 'Implement Winner'}</Button>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
