import { api } from 'src/boot/axios';

export interface TeamMember {
  id: number;
  name: string;
  role: string;
  bio: string;
  photo_url: string | null;
  order: number;
}

export const teamService = {
  async list(): Promise<TeamMember[]> {
    const { data } = await api.get<TeamMember[]>('/team/');
    return data;
  },
};
