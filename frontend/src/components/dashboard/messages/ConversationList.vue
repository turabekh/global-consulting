<template>
  <div class="gc-conv-list">
    <header class="gc-conv-list-header">
      <h2 class="gc-conv-list-title">{{ t('dashboard.messages.title') }}</h2>
      <span v-if="store.totalUnread > 0" class="gc-conv-list-unread">
        {{ store.totalUnread }}
      </span>
    </header>

    <div v-if="store.isLoading && !store.isLoaded" class="gc-conv-list-loading">
      <q-spinner color="primary" size="28px" />
    </div>

    <div v-else-if="store.conversations.length === 0" class="gc-conv-list-empty">
      <q-icon name="forum" size="32px" />
      <span class="gc-conv-list-empty-text">{{ t('dashboard.messages.empty') }}</span>
      <span class="gc-conv-list-empty-hint">{{ t('dashboard.messages.emptyHint') }}</span>
    </div>

    <ul v-else class="gc-conv-items">
      <li v-for="conv in store.conversations" :key="conv.id" class="gc-conv-item">
        <router-link
          :to="`/dashboard/messages/${conv.id}`"
          class="gc-conv-link"
          :class="{ 'gc-conv-link-active': activeId === conv.id }"
        >
          <div class="gc-conv-icon" :class="`gc-conv-icon-${conv.application_service_type}`">
            <q-icon :name="serviceIcon(conv.application_service_type)" size="18px" />
          </div>
          <div class="gc-conv-text">
            <div class="gc-conv-row">
              <span class="gc-conv-title">
                {{ conv.application_target_label || serviceLabel(conv.application_service_type) }}
              </span>
              <span v-if="conv.last_message_at" class="gc-conv-time">
                {{ formatRelative(conv.last_message_at, locale) }}
              </span>
            </div>
            <div class="gc-conv-row">
              <span class="gc-conv-preview">
                <strong v-if="conv.last_message?.sender_role === 'user'"
                  >{{ t('dashboard.messages.youLabel') }}:</strong
                >
                {{ conv.last_message?.body ?? t('dashboard.messages.threadEmpty') }}
              </span>
              <span v-if="conv.unread_count > 0" class="gc-conv-badge">
                {{ conv.unread_count }}
              </span>
            </div>
          </div>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { useMessagingStore } from 'src/stores/messaging';
import type { ServiceType } from 'src/services/applications';

defineProps<{ activeId: number | null }>();

const { t, locale } = useI18n();
const store = useMessagingStore();

function serviceLabel(type: ServiceType): string {
  return t(`dashboard.overview.serviceLabels.${type}`);
}

function serviceIcon(type: ServiceType): string {
  const map: Record<ServiceType, string> = {
    tourism: 'wb_sunny',
    study: 'menu_book',
    work: 'business_center',
    visa: 'description',
  };
  return map[type];
}

function formatRelative(iso: string, lang: string): string {
  const date = new Date(iso);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const minutes = Math.round(diffMs / 60000);

  if (minutes < 1) return lang === 'uz' ? 'hozir' : 'now';
  if (minutes < 60) return lang === 'uz' ? `${minutes} daq.` : `${minutes}m`;

  const hours = Math.round(minutes / 60);
  if (hours < 24) return lang === 'uz' ? `${hours} soat` : `${hours}h`;

  const days = Math.round(hours / 24);
  if (days < 7) return lang === 'uz' ? `${days} kun` : `${days}d`;

  return new Intl.DateTimeFormat(lang === 'uz' ? 'uz-UZ' : 'en-GB', {
    day: '2-digit',
    month: 'short',
  }).format(date);
}
</script>

<style scoped lang="scss">
.gc-conv-list {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.gc-conv-list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--gc-border);
}

.gc-conv-list-title {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-conv-list-unread {
  background: var(--gc-primary);
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 10px;
  border-radius: var(--gc-radius-pill);
}

.gc-conv-list-loading {
  display: flex;
  justify-content: center;
  padding: 32px 0;
}

.gc-conv-list-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px 24px;
  gap: 8px;
  text-align: center;
  color: var(--gc-text-muted);
}

.gc-conv-list-empty-text {
  font-size: 14px;
  font-weight: 600;
  margin-top: 8px;
  color: var(--gc-text);
}

.gc-conv-list-empty-hint {
  font-size: 13px;
}

.gc-conv-items {
  list-style: none;
  margin: 0;
  padding: 4px;
  flex: 1;
  overflow-y: auto;
}

.gc-conv-item {
  display: block;
}

.gc-conv-link {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: var(--gc-radius-md);
  text-decoration: none;
  color: inherit;
  transition: background 0.15s ease;

  &:hover {
    background: var(--gc-bg-soft);
  }
}

.gc-conv-link-active {
  background: var(--gc-primary-soft);

  &:hover {
    background: var(--gc-primary-soft);
  }
}

.gc-conv-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--gc-bg-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: var(--gc-primary);
}

.gc-conv-icon-tourism {
  color: #c97900;
}
.gc-conv-icon-study {
  color: var(--gc-primary);
}
.gc-conv-icon-work {
  color: #4a8dff;
}
.gc-conv-icon-visa {
  color: #d04848;
}

.gc-conv-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.gc-conv-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.gc-conv-title {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: -0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.gc-conv-time {
  font-size: 11px;
  color: var(--gc-text-muted);
  flex-shrink: 0;
}

.gc-conv-preview {
  font-size: 12px;
  color: var(--gc-text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.gc-conv-badge {
  background: var(--gc-primary);
  color: #ffffff;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: var(--gc-radius-pill);
  flex-shrink: 0;
}
</style>
