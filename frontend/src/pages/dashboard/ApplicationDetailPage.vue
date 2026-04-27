<template>
  <div v-if="loading" class="gc-detail-loading">
    <q-spinner color="primary" size="32px" />
  </div>

  <div v-else-if="!application" class="gc-detail-not-found">
    <h2 class="gc-detail-not-found-title">{{ t('dashboard.detail.empty') }}</h2>
    <q-btn
      outline
      no-caps
      :label="t('dashboard.detail.backToList')"
      to="/dashboard/applications"
      class="gc-detail-back-btn"
    />
  </div>

  <div v-else class="gc-detail">
    <router-link to="/dashboard/applications" class="gc-detail-back">
      <q-icon name="arrow_back" size="14px" />
      {{ t('dashboard.detail.backToList') }}
    </router-link>

    <header class="gc-detail-header">
      <div class="gc-detail-header-text">
        <span class="gc-detail-service">{{ serviceLabel }}</span>
        <h2 class="gc-detail-title">
          {{ application.target_label || serviceLabel }}
        </h2>
        <span class="gc-detail-ref">
          {{ t('dashboard.detail.referenceLabel') }}: <code>{{ shortReference }}</code>
        </span>
      </div>
      <div class="gc-detail-header-actions">
        <StatusBadge :status="application.status" />
        <q-btn
          v-if="conversationId"
          color="primary"
          unelevated
          no-caps
          icon="forum"
          :label="t('dashboard.detail.messageButton')"
          :to="`/dashboard/messages/${conversationId}`"
          class="gc-detail-message-btn"
        />
      </div>
    </header>

    <section class="gc-detail-meta-row">
      <div v-if="application.submitted_at" class="gc-detail-meta">
        <span class="gc-detail-meta-label">{{ t('dashboard.detail.submittedLabel') }}</span>
        <span class="gc-detail-meta-value">{{ formatDate(application.submitted_at, locale) }}</span>
      </div>
      <div v-if="application.decided_at" class="gc-detail-meta">
        <span class="gc-detail-meta-label">{{ t('dashboard.detail.decidedLabel') }}</span>
        <span class="gc-detail-meta-value">{{ formatDate(application.decided_at, locale) }}</span>
      </div>
      <div class="gc-detail-meta">
        <span class="gc-detail-meta-label">{{ t('dashboard.detail.lastUpdatedLabel') }}</span>
        <span class="gc-detail-meta-value">{{ formatDate(application.updated_at, locale) }}</span>
      </div>
    </section>

    <section v-if="application.team_message" class="gc-detail-team-msg">
      <div class="gc-detail-team-msg-icon">
        <q-icon name="chat_bubble" size="18px" />
      </div>
      <div class="gc-detail-team-msg-body">
        <span class="gc-detail-team-msg-label">{{ t('dashboard.detail.noteFromTeam') }}</span>
        <p class="gc-detail-team-msg-text">{{ application.team_message }}</p>
      </div>
    </section>

    <Step5Review :application="application" readonly @go-to-step="onUnusedStep" />

    <section v-if="canAddDocuments" class="gc-detail-docs-extra">
      <h3 class="gc-detail-docs-extra-title">{{ t('dashboard.detail.addMoreDocuments') }}</h3>
      <Step4Documents
        :reference="application.reference"
        :documents="application.documents"
        @documents-changed="loadApplication"
      />
    </section>

    <p v-else class="gc-detail-info">{{ t('dashboard.detail.cannotEdit') }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';
import { applicationsService, type ApplicationDetail } from 'src/services/applications';
import { formatDate } from 'src/utils/format';
import StatusBadge from 'src/components/dashboard/StatusBadge.vue';
import Step5Review from 'src/components/dashboard/application-steps/Step5Review.vue';
import Step4Documents from 'src/components/dashboard/application-steps/Step4Documents.vue';
import { useMessagingStore } from 'src/stores/messaging';

const { t, locale } = useI18n();
const route = useRoute();
const emit = defineEmits<{ 'page-title': [string] }>();
const messagingStore = useMessagingStore();

const conversationId = computed(() => {
  // Conversations are auto-created for every application via backend signal,
  // so we look it up by listing the user's conversations and matching the application reference.
  const reference = application.value?.reference;
  if (!reference) return null;
  const match = messagingStore.conversations.find((c) => c.application_reference === reference);
  return match?.id ?? null;
});
const application = ref<ApplicationDetail | null>(null);
const loading = ref(true);

const serviceLabel = computed(() => {
  if (!application.value) return '';
  return t(`dashboard.overview.serviceLabels.${application.value.service_type}`);
});

const shortReference = computed(() => {
  return application.value?.reference?.split('-')[0] ?? '';
});

const canAddDocuments = computed(() => {
  if (!application.value) return false;
  return ['submitted', 'in_review', 'needs_info'].includes(application.value.status);
});

async function loadApplication() {
  const reference = route.params.reference as string | undefined;
  if (!reference) {
    application.value = null;
    return;
  }
  loading.value = true;
  try {
    application.value = await applicationsService.detail(reference);
  } catch {
    application.value = null;
  } finally {
    loading.value = false;
  }
}

function onUnusedStep() {
  // No-op: edit jumps don't apply on the read-only detail page.
}

onMounted(async () => {
  await loadApplication();
  void messagingStore.load();
  emit('page-title', application.value?.target_label || t('dashboard.detail.titleFallback'));
});

watch(
  () => route.params.reference,
  () => loadApplication(),
);

watch(locale, () => {
  emit('page-title', application.value?.target_label || t('dashboard.detail.titleFallback'));
});
</script>

<style scoped lang="scss">
.gc-detail-loading,
.gc-detail-not-found {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 24px;
  gap: 16px;
  text-align: center;
}

.gc-detail-not-found-title {
  font-size: 22px;
  font-weight: 700;
  margin: 0;
}

.gc-detail-back-btn {
  border-radius: var(--gc-radius-pill);
  padding: 8px 24px;
  font-weight: 600;
}

.gc-detail {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.gc-detail-back {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--gc-text-muted);
  text-decoration: none;
  font-weight: 500;
  align-self: flex-start;

  &:hover {
    color: var(--gc-primary);
  }
}

.gc-detail-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.gc-detail-header-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-end;

  @media (max-width: 599px) {
    flex-direction: row;
    align-items: center;
    flex-wrap: wrap;
  }
}

.gc-detail-message-btn {
  border-radius: var(--gc-radius-pill);
  padding: 8px 18px;
  font-weight: 600;
}

.gc-detail-header-text {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.gc-detail-service {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gc-primary);
  font-weight: 600;
}

.gc-detail-title {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.2;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 30px;
  }
}

.gc-detail-ref {
  font-size: 12px;
  color: var(--gc-text-muted);

  code {
    font-family: monospace;
    background: var(--gc-bg-soft);
    padding: 1px 6px;
    border-radius: 4px;
  }
}

.gc-detail-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  padding: 16px 18px;
  background: var(--gc-bg);
  border: 1px solid var(--gc-border);
  border-radius: var(--gc-radius-md);
}

.gc-detail-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.gc-detail-meta-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gc-text-muted);
  font-weight: 600;
}

.gc-detail-meta-value {
  font-size: 14px;
  font-weight: 600;
}

.gc-detail-team-msg {
  display: flex;
  gap: 12px;
  padding: 16px 18px;
  background: var(--gc-primary-soft);
  border-radius: var(--gc-radius-md);
  border-left: 3px solid var(--gc-primary);
}

.gc-detail-team-msg-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--gc-bg);
  color: var(--gc-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.gc-detail-team-msg-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.gc-detail-team-msg-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 700;
  color: var(--gc-primary);
}

.gc-detail-team-msg-text {
  font-size: 14px;
  color: var(--gc-text);
  line-height: 1.5;
  margin: 0;
  white-space: pre-wrap;
}

.gc-detail-docs-extra {
  background: var(--gc-bg);
  border: 1px solid var(--gc-border);
  border-radius: var(--gc-radius-lg);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.gc-detail-docs-extra-title {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-detail-info {
  text-align: center;
  color: var(--gc-text-muted);
  font-size: 14px;
  margin: 24px 0;
}
</style>
