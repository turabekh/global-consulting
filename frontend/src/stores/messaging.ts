import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { messagingService, type ConversationListItem, type Message } from 'src/services/messaging';
import { messagingSocket, type IncomingEvent } from 'src/services/messaging-ws';

export const useMessagingStore = defineStore('messaging', () => {
  const conversations = ref<ConversationListItem[]>([]);
  const isLoading = ref(false);
  const isLoaded = ref(false);
  let unsubscribe: (() => void) | null = null;

  const totalUnread = computed(() =>
    conversations.value.reduce((sum, c) => sum + c.unread_count, 0),
  );

  async function load(force = false): Promise<void> {
    if (isLoaded.value && !force) return;
    isLoading.value = true;
    try {
      conversations.value = await messagingService.list();
      isLoaded.value = true;
    } finally {
      isLoading.value = false;
    }
  }

  function findConversation(id: number): ConversationListItem | undefined {
    return conversations.value.find((c) => c.id === id);
  }

  function applyIncomingMessage(conversationId: number, message: Message): void {
    const existing = findConversation(conversationId);
    if (!existing) {
      void load(true);
      return;
    }
    existing.last_message = {
      id: message.id,
      sender_role: message.sender_role,
      body: message.body,
      created_at: message.created_at,
    };
    existing.last_message_at = message.created_at;
    if (message.sender_role !== 'user') {
      existing.unread_count += 1;
    }
    conversations.value = [existing, ...conversations.value.filter((c) => c.id !== conversationId)];
  }

  async function markRead(id: number): Promise<void> {
    const existing = findConversation(id);
    if (!existing) return;
    existing.unread_count = 0;
    try {
      await messagingService.markRead(id);
    } catch {
      // best effort; keep local state in sync next reload
    }
  }

  function startListening(): void {
    if (unsubscribe) return;
    unsubscribe = messagingSocket.on((event: IncomingEvent) => {
      if (event.type === 'message_created') {
        applyIncomingMessage(event.conversation_id, event.message);
      }
    });
  }

  function stopListening(): void {
    if (unsubscribe) {
      unsubscribe();
      unsubscribe = null;
    }
  }

  function reset(): void {
    stopListening();
    conversations.value = [];
    isLoaded.value = false;
  }

  return {
    conversations,
    isLoading,
    isLoaded,
    totalUnread,
    load,
    findConversation,
    applyIncomingMessage,
    markRead,
    startListening,
    stopListening,
    reset,
  };
});
