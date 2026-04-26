import { api } from 'src/boot/axios';

export type ServiceType = 'tourism' | 'study' | 'work' | 'visa';

export type ApplicationStatus =
  | 'draft'
  | 'submitted'
  | 'in_review'
  | 'needs_info'
  | 'accepted'
  | 'rejected'
  | 'closed';

export type DocumentKind =
  | 'passport'
  | 'transcript'
  | 'cv'
  | 'financial'
  | 'certificate'
  | 'photo'
  | 'other';

export interface ApplicationDocument {
  id: number;
  kind: DocumentKind;
  file_url: string | null;
  original_filename: string;
  size_bytes: number;
  is_verified: boolean;
  uploaded_at: string;
}

export interface ApplicationListItem {
  reference: string;
  service_type: ServiceType;
  target_slug: string;
  target_label: string;
  status: ApplicationStatus;
  current_step: number;
  submitted_at: string | null;
  decided_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface ApplicationDetail extends ApplicationListItem {
  data: Record<string, unknown>;
  documents: ApplicationDocument[];
  team_message: string;
}
export interface ApplicationCreatePayload {
  service_type: ServiceType;
  target_slug?: string;
  target_label?: string;
  data?: Record<string, unknown>;
}

export interface ApplicationUpdatePayload {
  current_step?: number;
  data?: Record<string, unknown>;
  target_slug?: string;
  target_label?: string;
  service_type?: ServiceType;
}

export const applicationsService = {
  async list(): Promise<ApplicationListItem[]> {
    const { data } = await api.get<ApplicationListItem[] | { results: ApplicationListItem[] }>(
      '/applications/',
    );
    return Array.isArray(data) ? data : data.results;
  },

  async detail(reference: string): Promise<ApplicationDetail> {
    const { data } = await api.get<ApplicationDetail>(`/applications/${reference}/`);
    return data;
  },

  async create(payload: ApplicationCreatePayload): Promise<ApplicationDetail> {
    const { data } = await api.post<ApplicationDetail>('/applications/', payload);
    return data;
  },

  async update(reference: string, payload: ApplicationUpdatePayload): Promise<ApplicationDetail> {
    const { data } = await api.patch<ApplicationDetail>(`/applications/${reference}/`, payload);
    return data;
  },

  async submit(reference: string): Promise<ApplicationDetail> {
    const { data } = await api.post<ApplicationDetail>(`/applications/${reference}/submit/`);
    return data;
  },

  async remove(reference: string): Promise<void> {
    await api.delete(`/applications/${reference}/`);
  },

  async uploadDocument(
    reference: string,
    file: File,
    kind: DocumentKind = 'other',
  ): Promise<ApplicationDocument> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('kind', kind);
    const { data } = await api.post<ApplicationDocument>(
      `/applications/${reference}/documents/`,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } },
    );
    return data;
  },

  async deleteDocument(reference: string, documentId: number): Promise<void> {
    await api.delete(`/applications/${reference}/documents/${documentId}/`);
  },
};
