import { api } from 'src/boot/axios';

export type ServiceType = 'tourism' | 'study' | 'work' | 'visa' | 'other';

export interface ContactPayload {
  full_name: string;
  contact: string;
  service_type: ServiceType;
  note?: string;
}

export interface PartnershipPayload {
  company_name: string;
  contact: string;
  goals: string;
}

export const inquiriesService = {
  async submitContact(payload: ContactPayload): Promise<void> {
    await api.post('/inquiries/contact/', payload);
  },

  async submitPartnership(payload: PartnershipPayload): Promise<void> {
    await api.post('/inquiries/partnership/', payload);
  },
};
