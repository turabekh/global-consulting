<template>
  <div class="gc-messages-page">
    <div class="gc-messages-shell" :class="{ 'gc-messages-shell-thread-mode': hasActiveThread }">
      <aside
        class="gc-messages-sidebar"
        :class="{ 'gc-messages-sidebar-hidden-on-mobile': hasActiveThread }"
      >
        <ConversationList :active-id="activeId" />
      </aside>

      <div class="gc-messages-main">
        <ConversationThread v-if="activeId !== null" :key="activeId" :conversation-id="activeId" />
        <div v-else class="gc-messages-placeholder">
          <q-icon name="forum" size="32px" />
          <span>{{ t('dashboard.messages.selectThread') }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';
import ConversationList from 'src/components/dashboard/messages/ConversationList.vue';
import ConversationThread from 'src/components/dashboard/messages/ConversationThread.vue';
import { useMessagingStore } from 'src/stores/messaging';

const { t } = useI18n();
const route = useRoute();
const store = useMessagingStore();
const emit = defineEmits<{ 'page-title': [string] }>();

const activeId = computed<number | null>(() => {
  const raw = route.params.id;
  if (!raw) return null;
  const id = Number(Array.isArray(raw) ? raw[0] : raw);
  return Number.isFinite(id) ? id : null;
});

const hasActiveThread = computed(() => activeId.value !== null);

onMounted(() => {
  emit('page-title', t('dashboard.messages.title'));
  void store.load();
});

watch(
  () => t('dashboard.messages.title'),
  (val) => emit('page-title', val),
);
</script>

<style scoped lang="scss">
.gc-messages-page {
  margin: -24px -16px -64px;
  height: calc(100vh - 73px);
  display: flex;
  overflow: hidden;

  @media (min-width: 720px) {
    margin: -32px -32px -64px;
  }
}

.gc-messages-shell {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr;
  background: var(--gc-bg);
  min-height: 0;

  @media (min-width: 900px) {
    grid-template-columns: 320px 1fr;
  }
}

.gc-messages-sidebar {
  border-right: 1px solid var(--gc-border);
  background: var(--gc-bg);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.gc-messages-sidebar-hidden-on-mobile {
  @media (max-width: 899px) {
    display: none;
  }
}

.gc-messages-shell-thread-mode .gc-messages-main {
  @media (max-width: 899px) {
    display: flex;
  }
}

.gc-messages-main {
  display: flex;
  flex-direction: column;
  background: var(--gc-bg);
  min-width: 0;
  min-height: 0;
  overflow: hidden;

  @media (max-width: 899px) {
    display: none;
  }
}

.gc-messages-shell:not(.gc-messages-shell-thread-mode) .gc-messages-main {
  @media (max-width: 899px) {
    display: none;
  }
}

.gc-messages-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: var(--gc-text-muted);
  font-size: 14px;
  text-align: center;
}
</style>
