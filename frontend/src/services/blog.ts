import { api } from 'src/boot/axios';

export type BlogCategory = 'general' | 'tourism' | 'study' | 'work' | 'visa';

export interface BlogPostListItem {
  id: number;
  slug: string;
  title: string;
  excerpt: string;
  category: BlogCategory;
  cover_image_url: string | null;
  published_at: string | null;
  read_time_minutes: number;
}

export interface BlogPostDetail extends BlogPostListItem {
  body: string;
  body_html: string;
}

interface ListParams {
  category?: BlogCategory;
  limit?: number;
}

export const blogService = {
  async list(params: ListParams = {}): Promise<BlogPostListItem[]> {
    const { data } = await api.get<BlogPostListItem[] | { results: BlogPostListItem[] }>('/blog/', {
      params,
    });
    return Array.isArray(data) ? data : data.results;
  },

  async detail(slug: string): Promise<BlogPostDetail> {
    const { data } = await api.get<BlogPostDetail>(`/blog/${slug}/`);
    return data;
  },
};
