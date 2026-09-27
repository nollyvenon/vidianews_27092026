'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Heart, Users, MessageSquare, Search, Bell, BarChart3, Settings } from 'lucide-react';


interface SocialStats {
  totalInteractions: number;
  totalFollows: number;
  totalComments: number;
  totalMessages: number;
  totalNotifications: number;
  timestamp: string;
}


interface PlatformStat {
  id: number;
  metricName: string;
  metricValue: number;
  metricType: string;
  createdAt: string;
}


interface SearchResult {
  id: number;
  contentId: number;
  indexType: string;
  title: string;
  content: string;
  createdAt: string;
}


interface Notification {
  id: number;
  title: string;
  message: string;
  notificationType: string;
  createdAt: string;
}


export default function PlatformCompletionDashboard() {
  const [stats, setStats] = useState<SocialStats | null>(null);
  const [platformStats, setPlatformStats] = useState<PlatformStat[]>([]);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDays, setSelectedDays] = useState(7);

  useEffect(() => {
    fetchDashboardData();
  }, [selectedDays]);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [statsRes, platformStatsRes, notificationsRes] = await Promise.all([
        fetch('/api/v1/platform/dashboard-summary'),
        fetch(`/api/v1/platform/statistics?days=${selectedDays}&limit=100`),
        fetch('/api/v1/platform/system/notifications?limit=50'),
      ]);

      if (statsRes.ok) {
        setStats(await statsRes.json());
      }
      if (platformStatsRes.ok) {
        setPlatformStats(await platformStatsRes.json());
      }
      if (notificationsRes.ok) {
        setNotifications(await notificationsRes.json());
      }
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    try {
      const response = await fetch(
        `/api/v1/platform/search?query=${encodeURIComponent(searchQuery)}&limit=20`
      );
      if (response.ok) {
        setSearchResults(await response.json());
      }
    } catch (error) {
      console.error('Search failed:', error);
    }
  };

  return (
    <div className="w-full space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Platform Hub</h1>
        <p className="text-muted-foreground">Manage social features, search, notifications, and system analytics</p>
      </div>

      <Tabs defaultValue="overview" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="social">Social</TabsTrigger>
          <TabsTrigger value="search">Search</TabsTrigger>
          <TabsTrigger value="notifications">Notifications</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Interactions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div className="text-2xl font-bold">{stats?.totalInteractions || 0}</div>
                  <Heart className="h-4 w-4 text-muted-foreground" />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Follows</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div className="text-2xl font-bold">{stats?.totalFollows || 0}</div>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Comments</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div className="text-2xl font-bold">{stats?.totalComments || 0}</div>
                  <MessageSquare className="h-4 w-4 text-muted-foreground" />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Messages</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div className="text-2xl font-bold">{stats?.totalMessages || 0}</div>
                  <MessageSquare className="h-4 w-4 text-muted-foreground" />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">Notifications</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <div className="text-2xl font-bold">{stats?.totalNotifications || 0}</div>
                  <Bell className="h-4 w-4 text-muted-foreground" />
                </div>
              </CardContent>
            </Card>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Platform Statistics</CardTitle>
              <CardDescription>Last {selectedDays} days metrics</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex gap-2 mb-4">
                {[7, 14, 30].map((days) => (
                  <Button
                    key={days}
                    variant={selectedDays === days ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setSelectedDays(days)}
                  >
                    {days}d
                  </Button>
                ))}
              </div>

              {loading ? (
                <div className="text-center py-8">Loading...</div>
              ) : (
                <div className="space-y-4">
                  {platformStats.slice(0, 10).map((stat) => (
                    <div key={stat.id} className="flex items-center justify-between py-2 border-b last:border-0">
                      <div className="flex items-center gap-2">
                        <BarChart3 className="h-4 w-4 text-muted-foreground" />
                        <div>
                          <p className="font-medium text-sm">{stat.metricName}</p>
                          <p className="text-xs text-muted-foreground">{stat.metricType}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold">{stat.metricValue.toFixed(2)}</p>
                        <p className="text-xs text-muted-foreground">{new Date(stat.createdAt).toLocaleDateString()}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="social" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Social Features</CardTitle>
              <CardDescription>Manage user interactions, follows, and comments</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-base">Interactions</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Button variant="outline" className="w-full">View All Interactions</Button>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-base">Follows</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Button variant="outline" className="w-full">View Followers</Button>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-base">Comments</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Button variant="outline" className="w-full">Moderate Comments</Button>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-base">Messages</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Button variant="outline" className="w-full">View Messages</Button>
                  </CardContent>
                </Card>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="search" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Content Search</CardTitle>
              <CardDescription>Search and manage indexed content</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <form onSubmit={handleSearch} className="flex gap-2">
                <Input
                  placeholder="Search content..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <Button type="submit" variant="default">
                  <Search className="h-4 w-4 mr-2" />
                  Search
                </Button>
              </form>

              {searchResults.length > 0 && (
                <div className="space-y-2">
                  {searchResults.map((result) => (
                    <div key={result.id} className="p-4 border rounded-lg hover:bg-muted/50">
                      <h3 className="font-medium">{result.title}</h3>
                      <p className="text-sm text-muted-foreground line-clamp-2">{result.content}</p>
                      <div className="flex items-center gap-2 mt-2">
                        <Badge variant="secondary">{result.indexType}</Badge>
                        <span className="text-xs text-muted-foreground">
                          {new Date(result.createdAt).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="notifications" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Notifications</CardTitle>
              <CardDescription>Push notifications and system alerts</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {notifications.length > 0 ? (
                  notifications.slice(0, 10).map((notif) => (
                    <div key={notif.id} className="p-3 border rounded-lg">
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="font-medium text-sm">{notif.title}</p>
                          <p className="text-sm text-muted-foreground">{notif.message}</p>
                        </div>
                        <Badge variant="outline">{notif.notificationType}</Badge>
                      </div>
                      <p className="text-xs text-muted-foreground mt-2">
                        {new Date(notif.createdAt).toLocaleString()}
                      </p>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-muted-foreground">No notifications</div>
                )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Notification Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" className="w-full">Broadcast System Notification</Button>
              <Button variant="outline" className="w-full">Configure Notification Rules</Button>
              <Button variant="outline" className="w-full">View Delivery Reports</Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5" />
            Admin Controls
          </CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Button variant="outline" className="w-full">Manage Users</Button>
          <Button variant="outline" className="w-full">Moderation Queue</Button>
          <Button variant="outline" className="w-full">Audit Logs</Button>
          <Button variant="outline" className="w-full">System Config</Button>
          <Button variant="outline" className="w-full">Compliance Rules</Button>
          <Button variant="outline" className="w-full">Security Settings</Button>
        </CardContent>
      </Card>
    </div>
  );
}
