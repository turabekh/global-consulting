<template>
  <div class="gc-thread">
    <header class="gc-thread-header">
      <router-link to="/dashboard/messages" class="gc-thread-back">
        <q-icon name="arrow_back" size="16px" />
      </router-link>
      <div class="gc-thread-header-text">
        <span class="gc-thread-regarding">{{ t('dashboard.messages.regardingLabel') }}</span>
        <h3 class="gc-thread-title">
          {{ thread?.application_target_label || serviceLabel }}
        </h3>
      </div>
    </header>

    <div ref="bodyEl" class="gc-thread-body">
      <div v-if="loading" class="gc-thread-loading">
        <q-spinner color="primary" size="28px" />
      </div>

      <p v-else-if="!thread || thread.messages.length === 0" class="gc-thread-empty">
        {{ t('dashboard.messages.threadEmpty') }}
      </p>

      <ul v-else class="gc-thread-list">
        <li
          v-for="msg in thread.messages"
          :key="msg.id"
          class="gc-thread-message"
          :class="`gc-thread-message-${msg.sender_role}`"
        >
          <span class="gc-thread-bubble">{{ msg.body }}</span>
          <span class="gc-thread-meta">
            {{ senderLabel(msg.sender_role) }}{{ t('dashboard.messages.atTime')
            }}{{ formatTime(msg.created_at, locale) }}
          </span>
        </li>
      </ul>
    </div>

    <footer class="gc-thread-footer">
      <q-input
        v-model="draft"
        outlined
        dense
        autogrow
        :placeholder="t('dashboard.messages.placeholder')"
        :disable="!thread || sending"
        class="gc-thread-input"
        @keydown.enter.prevent="onEnter"
      />
      <q-btn
        color="primary"
        unelevated
        no-caps
        :label="sending ? t('dashboard.messages.sending') : t('dashboard.messages.send')"
        :loading="sending"
        :disable="!canSend"
        class="gc-thread-send"
        @click="onSend"
      />
    </footer>

    <q-banner v-if="error" class="gc-error-banner gc-thread-error" dense rounded>
      {{ error }}
    </q-banner>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { messagingService, type ConversationDetail, type SenderRole } from 'src/services/messaging';
import { messagingSocket, type IncomingEvent } from 'src/services/messaging-ws';
import { useMessagingStore } from 'src/stores/messaging';
import { extractApiError } from 'src/utils/api-errors';

interface Props {
  conversationId: number;
}

const props = defineProps<Props>();

const { t, locale } = useI18n();
const store = useMessagingStore();

const thread = ref<ConversationDetail | null>(null);
const loading = ref(true);
const draft = ref('');
const sending = ref(false);
const error = ref<string | null>(null);
const bodyEl = ref<HTMLElement | null>(null);
let unsubscribe: (() => void) | null = null;

const serviceLabel = computed(() => {
  if (!thread.value) return '';
  return t(`dashboard.overview.serviceLabels.${thread.value.application_service_type}`);
});

const canSend = computed(() => draft.value.trim().length > 0 && !sending.value);

async function loadThread() {
  loading.value = true;
  try {
    thread.value = await messagingService.detail(props.conversationId);
    await store.markRead(props.conversationId);
    await scrollToBottom();
  } catch {
    thread.value = null;
  } finally {
    loading.value = false;
  }
}

async function scrollToBottom() {
  await nextTick();
  if (bodyEl.value) {
    bodyEl.value.scrollTop = bodyEl.value.scrollHeight;
  }
}

function senderLabel(role: SenderRole): string {
  if (role === 'user') return t('dashboard.messages.youLabel');
  if (role === 'staff') return t('dashboard.messages.teamLabel');
  return t('dashboard.messages.systemLabel');
}

function formatTime(iso: string, lang: string): string {
  return new Intl.DateTimeFormat(lang === 'uz' ? 'uz-UZ' : 'en-GB', {
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(iso));
}

async function onSend() {
  if (!thread.value || !canSend.value) return;
  const body = draft.value.trim();
  error.value = null;
  sending.value = true;

  draft.value = '';

  try {
    const real = await messagingService.send(props.conversationId, body);
    if (thread.value) {
      const exists = thread.value.messages.some((m) => m.id === real.id);
      if (!exists) {
        thread.value.messages.push(real);
        await scrollToBottom();
      }
    }
    store.applyIncomingMessage(props.conversationId, real);
  } catch (err) {
    draft.value = body;
    error.value = extractApiError(err, t('dashboard.messages.sendError'));
  } finally {
    sending.value = false;
  }
}

function onEnter(event: KeyboardEvent) {
  if (event.shiftKey) return;
  void onSend();
}

function onIncoming(event: IncomingEvent) {
  if (event.type !== 'message_created') return;
  if (event.conversation_id !== props.conversationId) return;
  if (!thread.value) return;
  const exists = thread.value.messages.some((m) => m.id === event.message.id);
  if (exists) return;
  thread.value.messages.push(event.message);
  void store.markRead(props.conversationId);
  void scrollToBottom();
}

onMounted(() => {
  unsubscribe = messagingSocket.on(onIncoming);
  void loadThread();
});

onUnmounted(() => {
  if (unsubscribe) unsubscribe();
});

watch(
  () => props.conversationId,
  () => loadThread(),
);
</script>

<style scoped lang="scss">
.gc-thread {
  display: flex;
  flex-direction: column;
  height: 94%;
  background: var(--gc-bg);

  @media (max-width: 899px) {
    height: 100%;
  }
}

.gc-thread-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--gc-border);
}

.gc-thread-back {
  display: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--gc-bg-soft);
  color: var(--gc-text);
  align-items: center;
  justify-content: center;
  text-decoration: none;
  flex-shrink: 0;

  @media (max-width: 899px) {
    display: flex;
  }
}

.gc-thread-header-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.gc-thread-regarding {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gc-text-muted);
  font-weight: 600;
}

.gc-thread-title {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.gc-thread-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: var(--gc-bg-soft);
}

.gc-thread-loading,
.gc-thread-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--gc-text-muted);
}

.gc-thread-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gc-thread-message {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-width: 75%;
}

.gc-thread-message-user {
  align-self: flex-end;
  align-items: flex-end;
}

.gc-thread-message-staff,
.gc-thread-message-system {
  align-self: flex-start;
  align-items: flex-start;
}

.gc-thread-bubble {
  padding: 10px 14px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.gc-thread-message-user .gc-thread-bubble {
  background: var(--gc-primary);
  color: #ffffff;
  border-bottom-right-radius: 4px;
}

.gc-thread-message-staff .gc-thread-bubble {
  background: var(--gc-bg);
  color: var(--gc-text);
  border: 1px solid var(--gc-border);
  border-bottom-left-radius: 4px;
}

.gc-thread-message-system .gc-thread-bubble {
  background: transparent;
  color: var(--gc-text-muted);
  font-style: italic;
  font-size: 12px;
}

.gc-thread-meta {
  font-size: 11px;
  color: var(--gc-text-muted);
  padding: 0 8px;
}

.gc-thread-footer {
  display: flex;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid var(--gc-border);
  align-items: flex-end;
}

.gc-thread-input {
  flex: 1;
}

.gc-thread-send {
  border-radius: var(--gc-radius-pill);
  padding: 8px 24px;
  font-weight: 600;
}

.gc-thread-error {
  margin: 8px 20px 16px;
}
</style>
