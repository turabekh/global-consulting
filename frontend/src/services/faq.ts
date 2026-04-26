import { api } from 'src/boot/axios';

export type FAQCategory = 'general' | 'tourism' | 'study' | 'work' | 'visa';

export interface FAQ {
  id: number;
  category: FAQCategory;
  question: string;
  answer: string;
  answer_html: string;
  order: number;
}

export const faqService = {
  async list(category?: FAQCategory): Promise<FAQ[]> {
    const params = category ? { category } : {};
    const { data } = await api.get<FAQ[]>('/faq/', { params });
    return data;
  },
};
