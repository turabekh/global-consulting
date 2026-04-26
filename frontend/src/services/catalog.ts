import { api } from 'src/boot/axios';

export type Currency = 'USD' | 'EUR' | 'UZS';
export type EmploymentType = 'full_time' | 'part_time' | 'contract' | 'internship';
export type VisaCategory = 'tourist' | 'student' | 'work' | 'business' | 'family';

export interface TourPackage {
  id: number;
  slug: string;
  title: string;
  destination: string;
  description: string;
  duration_days: number;
  price_from: string | null;
  currency: Currency;
  tag_list: string[];
  cover_image_url: string | null;
}

export interface TourPackageDetail extends TourPackage {
  body: string;
  body_html: string;
}

export interface University {
  id: number;
  slug: string;
  title: string;
  country: string;
  city: string;
  description: string;
  tuition_from: string | null;
  currency: Currency;
  world_ranking: number | null;
  cover_image_url: string | null;
}

export interface UniversityDetail extends University {
  body: string;
  body_html: string;
  programs_offered: string;
  programs_offered_html: string;
}

export interface Job {
  id: number;
  slug: string;
  title: string;
  country: string;
  city: string;
  industry: string;
  description: string;
  salary_from: string | null;
  salary_to: string | null;
  currency: Currency;
  employment_type: EmploymentType;
  cover_image_url: string | null;
}

export interface JobDetail extends Job {
  body: string;
  body_html: string;
}

export interface VisaType {
  id: number;
  slug: string;
  title: string;
  country: string;
  category: VisaCategory;
  description: string;
  processing_time: string;
  success_rate: number | null;
  cover_image_url: string | null;
}

export interface VisaTypeDetail extends VisaType {
  body: string;
  body_html: string;
}

export const tourPackagesService = {
  async list(): Promise<TourPackage[]> {
    const { data } = await api.get<TourPackage[]>('/tour-packages/');
    return data;
  },
  async detail(slug: string): Promise<TourPackageDetail> {
    const { data } = await api.get<TourPackageDetail>(`/tour-packages/${slug}/`);
    return data;
  },
};

export const universitiesService = {
  async list(): Promise<University[]> {
    const { data } = await api.get<University[]>('/universities/');
    return data;
  },
  async detail(slug: string): Promise<UniversityDetail> {
    const { data } = await api.get<UniversityDetail>(`/universities/${slug}/`);
    return data;
  },
};

export const jobsService = {
  async list(): Promise<Job[]> {
    const { data } = await api.get<Job[]>('/jobs/');
    return data;
  },
  async detail(slug: string): Promise<JobDetail> {
    const { data } = await api.get<JobDetail>(`/jobs/${slug}/`);
    return data;
  },
};

export const visaTypesService = {
  async list(): Promise<VisaType[]> {
    const { data } = await api.get<VisaType[]>('/visa-types/');
    return data;
  },
  async detail(slug: string): Promise<VisaTypeDetail> {
    const { data } = await api.get<VisaTypeDetail>(`/visa-types/${slug}/`);
    return data;
  },
};
