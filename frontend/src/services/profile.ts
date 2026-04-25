import { api } from 'src/boot/axios';
import type { User } from 'src/services/auth';

export interface ProfileUpdatePayload {
  first_name?: string;
  last_name?: string;
  phone?: string;
  profile?: {
    language?: string;
    timezone?: string;
    bio?: string;
  };
}

export const profileService = {
  async fetchMe(): Promise<User> {
    const { data } = await api.get<User>('/users/me/');
    return data;
  },

  async updateMe(payload: ProfileUpdatePayload): Promise<User> {
    const { data } = await api.patch<User>('/users/me/', payload);
    return data;
  },

  async uploadAvatar(file: File): Promise<User> {
    const formData = new FormData();
    formData.append('profile.avatar', file);
    const { data } = await api.patch<User>('/users/me/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return data;
  },
};
