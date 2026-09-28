import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { BookmarkIcon, ThumbsUp } from 'lucide-react';

export default function RecommendationsTab() {
  const recommendations = [
    { id: 1, title: 'AI and Machine Learning Trends', score: 92, category: 'Technology' },
    { id: 2, title: 'Cloud Infrastructure Guide', score: 87, category: 'DevOps' },
    { id: 3, title: 'Security Best Practices 2026', score: 85, category: 'Security' },
    { id: 4, title: 'Data Science for Business', score: 78, category: 'Analytics' },
    { id: 5, title: 'API Design Patterns', score: 76, category: 'Backend' },
  ];

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Recommendation Engine</CardTitle>
          <CardDescription>AI-powered content recommendations for your audience</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {recommendations.map((rec) => (
              <div key={rec.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition">
                <div className="flex-1">
                  <h4 className="font-medium">{rec.title}</h4>
                  <div className="flex gap-2 mt-2">
                    <Badge variant="outline">{rec.category}</Badge>
                    <Badge className="bg-blue-100 text-blue-800">{rec.score}% match</Badge>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button size="sm" variant="ghost">
                    <BookmarkIcon className="h-4 w-4" />
                  </Button>
                  <Button size="sm" variant="ghost">
                    <ThumbsUp className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>User Preferences</CardTitle>
          <CardDescription>Tracked user interests and preferences</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {['Technology', 'DevOps', 'Security', 'Cloud Computing', 'Machine Learning'].map((pref, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <span className="text-sm font-medium">{pref}</span>
                <div className="flex gap-2">
                  <span className="text-sm text-gray-600">45 interactions</span>
                  <Button size="sm" variant="ghost" className="h-6">×</Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Performance Metrics</CardTitle>
          <CardDescription>Recommendation click-through and engagement</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-blue-50 rounded">
              <p className="text-sm text-gray-600 mb-1">Recommendation CTR</p>
              <p className="text-2xl font-bold">6.8%</p>
            </div>
            <div className="p-4 bg-green-50 rounded">
              <p className="text-sm text-gray-600 mb-1">Avg Click-to-Read</p>
              <p className="text-2xl font-bold">2.3 min</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
