import { api } from 'src/boot/axios';

export interface Testimonial {
  id: number;
  author_name: string;
  author_city: string;
  author_photo_url: string | null;
  body: string;
  body_html: string;
  order: number;
}

export const testimonialsService = {
  async list(): Promise<Testimonial[]> {
    const { data } = await api.get<Testimonial[]>('/testimonials/');
    return data;
  },
};
