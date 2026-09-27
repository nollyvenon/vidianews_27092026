'use client';

export interface ContentCreateRequest {
  title: string;
  slug: string;
  description?: string;
  body?: string;
  content_type: 'video' | 'article' | 'blog_post' | 'newsletter';
  category_id?: number;
  thumbnail_url?: string;
  featured_image_url?: string;
  status?: 'draft' | 'published' | 'scheduled';
  access_level?: 'public' | 'members_only' | 'premium' | 'private';
  tag_ids?: number[];
  seo_title?: string;
  seo_description?: string;
  seo_keywords?: string;
}

export interface ContentUpdateRequest extends Partial<ContentCreateRequest> {}

export interface ContentResponse {
  id: number;
  title: string;
  slug: string;
  description: string;
  body?: string;
  content_type: string;
  status: string;
  access_level: string;
  views_count: number;
  likes_count: number;
  comments_count: number;
  shares_count: number;
  thumbnail_url?: string;
  featured_image_url?: string;
  created_at: string;
  updated_at: string;
  published_at?: string;
}

class ContentService {
  private baseUrl = '/api/v1/content';
  private getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    };
  }

  async createContent(data: ContentCreateRequest): Promise<ContentResponse> {
    const response = await fetch(this.baseUrl, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
    });

    if (!response.ok) throw new Error('Failed to create content');
    return response.json();
  }

  async updateContent(id: number, data: ContentUpdateRequest): Promise<ContentResponse> {
    const response = await fetch(`${this.baseUrl}/${id}`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(data),
    });

    if (!response.ok) throw new Error('Failed to update content');
    return response.json();
  }

  async getContent(id: number): Promise<ContentResponse> {
    const response = await fetch(`${this.baseUrl}/${id}`);
    if (!response.ok) throw new Error('Failed to fetch content');
    return response.json();
  }

  async getContentBySlug(slug: string): Promise<ContentResponse> {
    const response = await fetch(`${this.baseUrl}/by-slug/${slug}`);
    if (!response.ok) throw new Error('Failed to fetch content');
    return response.json();
  }

  async deleteContent(id: number): Promise<void> {
    const response = await fetch(`${this.baseUrl}/${id}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });

    if (!response.ok) throw new Error('Failed to delete content');
  }

  async listContent(filters?: {
    page?: number;
    page_size?: number;
    status?: string;
    content_type?: string;
    category_id?: number;
  }): Promise<{ items: ContentResponse[]; total: number }> {
    const params = new URLSearchParams();
    if (filters?.page) params.append('page', String(filters.page));
    if (filters?.page_size) params.append('page_size', String(filters.page_size));
    if (filters?.status) params.append('status', filters.status);
    if (filters?.content_type) params.append('content_type', filters.content_type);
    if (filters?.category_id) params.append('category_id', String(filters.category_id));

    const response = await fetch(`${this.baseUrl}?${params}`);
    if (!response.ok) throw new Error('Failed to fetch content list');
    return response.json();
  }

  async searchContent(query: string, limit?: number): Promise<ContentResponse[]> {
    const params = new URLSearchParams({ query });
    if (limit) params.append('limit', String(limit));

    const response = await fetch(`${this.baseUrl}/search?${params}`);
    if (!response.ok) throw new Error('Failed to search content');
    return response.json();
  }

  async getFeaturedContent(limit?: number): Promise<ContentResponse[]> {
    const params = new URLSearchParams();
    if (limit) params.append('limit', String(limit));

    const response = await fetch(`${this.baseUrl}/featured?${params}`);
    if (!response.ok) throw new Error('Failed to fetch featured content');
    return response.json();
  }

  async getTrendingContent(days?: number, limit?: number): Promise<ContentResponse[]> {
    const params = new URLSearchParams();
    if (days) params.append('days', String(days));
    if (limit) params.append('limit', String(limit));

    const response = await fetch(`${this.baseUrl}/trending?${params}`);
    if (!response.ok) throw new Error('Failed to fetch trending content');
    return response.json();
  }

  async publishContent(id: number, accessLevel?: string): Promise<ContentResponse> {
    const response = await fetch(`${this.baseUrl}/${id}/publish`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ access_level: accessLevel || 'public' }),
    });

    if (!response.ok) throw new Error('Failed to publish content');
    return response.json();
  }

  async scheduleContent(id: number, scheduledAt: Date): Promise<ContentResponse> {
    const response = await fetch(`${this.baseUrl}/${id}/schedule`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ scheduled_at: scheduledAt.toISOString() }),
    });

    if (!response.ok) throw new Error('Failed to schedule content');
    return response.json();
  }

  async archiveContent(id: number): Promise<ContentResponse> {
    const response = await fetch(`${this.baseUrl}/${id}/archive`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({}),
    });

    if (!response.ok) throw new Error('Failed to archive content');
    return response.json();
  }

  async addVideo(contentId: number, sourceUrl: string): Promise<any> {
    const response = await fetch(`${this.baseUrl}/${contentId}/videos`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ source_url: sourceUrl }),
    });

    if (!response.ok) throw new Error('Failed to add video');
    return response.json();
  }

  async addMediaFile(contentId: number, fileData: any): Promise<any> {
    const response = await fetch(`${this.baseUrl}/${contentId}/media`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify(fileData),
    });

    if (!response.ok) throw new Error('Failed to add media file');
    return response.json();
  }

  async recordEngagement(contentId: number, engagementType: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/${contentId}/engage`, {
      method: 'POST',
      body: JSON.stringify({ engagement_type: engagementType }),
    });

    if (!response.ok) console.error('Failed to record engagement');
  }

  async getContentStats(id: number): Promise<any> {
    const response = await fetch(`${this.baseUrl}/${id}/stats`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  }

  async bulkUpdateContent(ids: number[], updates: any): Promise<{ updated: number }> {
    const response = await fetch(`${this.baseUrl}/bulk/update`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({
        content_ids: ids,
        ...updates,
      }),
    });

    if (!response.ok) throw new Error('Failed to bulk update');
    return response.json();
  }

  async bulkDeleteContent(ids: number[]): Promise<{ deleted: number }> {
    const response = await fetch(`${this.baseUrl}/bulk/delete`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ content_ids: ids }),
    });

    if (!response.ok) throw new Error('Failed to bulk delete');
    return response.json();
  }
}

export const contentService = new ContentService();
