'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import { Loader2, Plus, Search, Edit2, Trash2, Eye, Share2 } from 'lucide-react';

interface Content {
  id: number;
  title: string;
  slug: string;
  description: string;
  content_type: 'video' | 'article' | 'blog_post' | 'newsletter';
  status: 'draft' | 'scheduled' | 'published' | 'archived';
  views_count: number;
  likes_count: number;
  created_at: string;
  published_at: string | null;
  thumbnail_url: string | null;
}

export default function ContentPage() {
  const router = useRouter();
  const { toast } = useToast();
  const [content, setContent] = useState<Content[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [typeFilter, setTypeFilter] = useState<string>('');
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    fetchContent();
  }, [page, statusFilter, typeFilter]);

  const fetchContent = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams({
        page: page.toString(),
        page_size: '20',
      });

      if (statusFilter) params.append('status', statusFilter);
      if (typeFilter) params.append('content_type', typeFilter);

      const response = await fetch(`/api/v1/content?${params}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (!response.ok) throw new Error('Failed to fetch content');
      const data = await response.json();
      setContent(data.items || []);
      setTotal(data.total || 0);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to fetch content',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) {
      fetchContent();
      return;
    }

    try {
      const response = await fetch(
        `/api/v1/content/search?query=${encodeURIComponent(searchQuery)}`,
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
          },
        }
      );

      if (!response.ok) throw new Error('Search failed');
      const results = await response.json();
      setContent(results);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Search failed',
        variant: 'destructive',
      });
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this content?')) return;

    try {
      const response = await fetch(`/api/v1/content/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      if (!response.ok) throw new Error('Delete failed');
      toast({
        title: 'Success',
        description: 'Content deleted successfully',
      });
      fetchContent();
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to delete content',
        variant: 'destructive',
      });
    }
  };

  const getStatusBadgeColor = (status: string) => {
    switch (status) {
      case 'published':
        return 'bg-green-100 text-green-800';
      case 'scheduled':
        return 'bg-blue-100 text-blue-800';
      case 'draft':
        return 'bg-gray-100 text-gray-800';
      case 'archived':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'video':
        return '🎥';
      case 'article':
        return '📄';
      case 'blog_post':
        return '📝';
      case 'newsletter':
        return '📧';
      default:
        return '📄';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Content Management</h1>
          <p className="text-gray-500">Create, edit, and manage your content</p>
        </div>
        <Link href="/dashboard/content/new">
          <Button className="gap-2">
            <Plus size={20} />
            New Content
          </Button>
        </Link>
      </div>

      {/* Filters and Search */}
      <Card>
        <CardContent className="pt-6">
          <form onSubmit={handleSearch} className="space-y-4">
            <div className="flex gap-4">
              <div className="flex-1">
                <Input
                  placeholder="Search content by title..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full"
                />
              </div>
              <Button type="submit" variant="outline" className="gap-2">
                <Search size={20} />
                Search
              </Button>
            </div>

            <div className="flex gap-4">
              <select
                value={statusFilter}
                onChange={(e) => {
                  setStatusFilter(e.target.value);
                  setPage(1);
                }}
                className="px-3 py-2 border rounded-md"
              >
                <option value="">All Status</option>
                <option value="draft">Draft</option>
                <option value="published">Published</option>
                <option value="scheduled">Scheduled</option>
                <option value="archived">Archived</option>
              </select>

              <select
                value={typeFilter}
                onChange={(e) => {
                  setTypeFilter(e.target.value);
                  setPage(1);
                }}
                className="px-3 py-2 border rounded-md"
              >
                <option value="">All Types</option>
                <option value="video">Video</option>
                <option value="article">Article</option>
                <option value="blog_post">Blog Post</option>
                <option value="newsletter">Newsletter</option>
              </select>
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Content List */}
      {loading ? (
        <div className="flex justify-center py-12">
          <Loader2 className="animate-spin" size={32} />
        </div>
      ) : content.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center">
            <p className="text-gray-500">No content found</p>
            <Link href="/dashboard/content/new">
              <Button className="mt-4">Create First Content</Button>
            </Link>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {content.map((item) => (
            <Card key={item.id}>
              <CardContent className="py-4">
                <div className="flex gap-4">
                  {item.thumbnail_url && (
                    <img
                      src={item.thumbnail_url}
                      alt={item.title}
                      className="w-24 h-24 object-cover rounded"
                    />
                  )}
                  <div className="flex-1">
                    <div className="flex gap-2 items-start justify-between">
                      <div className="flex-1">
                        <div className="flex gap-2 items-center">
                          <span className="text-xl">{getTypeIcon(item.content_type)}</span>
                          <h3 className="text-lg font-semibold">{item.title}</h3>
                        </div>
                        <p className="text-sm text-gray-500 mt-1">{item.description}</p>
                        <div className="flex gap-2 mt-2">
                          <Badge className={getStatusBadgeColor(item.status)}>
                            {item.status}
                          </Badge>
                          {item.published_at && (
                            <Badge variant="outline" className="text-xs">
                              {new Date(item.published_at).toLocaleDateString()}
                            </Badge>
                          )}
                        </div>
                      </div>
                      <div className="flex gap-2 flex-col">
                        <div className="text-right text-sm text-gray-500">
                          <div className="flex items-center gap-1 justify-end">
                            <Eye size={16} />
                            {item.views_count}
                          </div>
                          <div className="flex items-center gap-1 justify-end">
                            ❤️ {item.likes_count}
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2 mt-4">
                      <Link href={`/dashboard/content/${item.id}/edit`}>
                        <Button size="sm" variant="outline" className="gap-2">
                          <Edit2 size={16} />
                          Edit
                        </Button>
                      </Link>
                      <Link href={`/dashboard/content/${item.id}`}>
                        <Button size="sm" variant="outline" className="gap-2">
                          <Eye size={16} />
                          View
                        </Button>
                      </Link>
                      <Button
                        size="sm"
                        variant="outline"
                        className="gap-2"
                        onClick={() => handleDelete(item.id)}
                      >
                        <Trash2 size={16} />
                        Delete
                      </Button>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}

          {/* Pagination */}
          <div className="flex justify-between items-center mt-6">
            <Button
              disabled={page === 1}
              onClick={() => setPage(p => p - 1)}
              variant="outline"
            >
              Previous
            </Button>
            <span className="text-sm text-gray-500">
              Page {page} of {Math.ceil(total / 20)}
            </span>
            <Button
              disabled={page * 20 >= total}
              onClick={() => setPage(p => p + 1)}
              variant="outline"
            >
              Next
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
