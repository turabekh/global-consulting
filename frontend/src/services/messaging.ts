import { api } from 'src/boot/axios';
import type { ApplicationStatus, ServiceType } from 'src/services/applications';

export type SenderRole = 'user' | 'staff' | 'system';

export interface Message {
  id: number;
  sender_role: SenderRole;
  author: number | null;
  body: string;
  created_at: string;
}

export interface LastMessagePreview {
  id: number;
  sender_role: SenderRole;
  body: string;
  created_at: string;
}

export interface ConversationListItem {
  id: number;
  application_reference: string;
  application_target_label: string;
  application_service_type: ServiceType;
  application_status: ApplicationStatus;
  last_message_at: string | null;
  last_message: LastMessagePreview | null;
  unread_count: number;
}

export interface ConversationDetail extends ConversationListItem {
  messages: Message[];
}

export const messagingService = {
  async list(): Promise<ConversationListItem[]> {
    const { data } = await api.get<ConversationListItem[] | { results: ConversationListItem[] }>(
      '/conversations/',
    );
    return Array.isArray(data) ? data : data.results;
  },

  async detail(id: number): Promise<ConversationDetail> {
    const { data } = await api.get<ConversationDetail>(`/conversations/${id}/`);
    return data;
  },

  async send(id: number, body: string): Promise<Message> {
    const { data } = await api.post<Message>(`/conversations/${id}/messages/`, { body });
    return data;
  },

  async markRead(id: number): Promise<void> {
    await api.post(`/conversations/${id}/mark-read/`);
  },
};
