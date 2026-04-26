<template>
  <div v-if="loading" class="gc-edit-loading">
    <q-spinner color="primary" size="32px" />
  </div>

  <div v-else-if="!application" class="gc-edit-not-found">
    <h2 class="gc-edit-not-found-title">{{ t('pages.blogDetail.notFound') }}</h2>
    <q-btn
      outline
      no-caps
      :label="t('dashboard.list.title')"
      to="/dashboard/applications"
      class="gc-edit-back-btn"
    />
  </div>

  <div v-else-if="submitted" class="gc-edit-submitted">
    <div class="gc-edit-submitted-icon">
      <q-icon name="check" size="36px" />
    </div>
    <h2 class="gc-edit-submitted-title">{{ t('dashboard.edit.submittedTitle') }}</h2>
    <p class="gc-edit-submitted-text">{{ t('dashboard.edit.submittedMessage') }}</p>
    <q-btn
      color="primary"
      unelevated
      no-caps
      :label="t('dashboard.edit.submittedAction')"
      to="/dashboard/applications"
      class="gc-edit-submitted-btn"
    />
  </div>

  <div v-else class="gc-edit-page">
    <div class="gc-edit-shell">
      <header class="gc-edit-header">
        <h2 class="gc-edit-title">{{ headerTitle }}</h2>
        <p v-if="application.target_label" class="gc-edit-subtitle">
          {{ application.target_label }}
        </p>
      </header>

      <ApplicationStepIndicator :current="currentStep" :steps="STEPS" />

      <div class="gc-edit-step">
        <div class="gc-edit-step-stub">
          <p class="gc-edit-step-stub-text">Step {{ currentStep }} content goes here.</p>
        </div>
      </div>

      <q-banner v-if="error" class="gc-error-banner" dense rounded>{{ error }}</q-banner>

      <footer class="gc-edit-footer">
        <q-btn
          flat
          no-caps
          icon="arrow_back"
          :label="t('dashboard.edit.back')"
          :disable="currentStep === 1 || saving"
          class="gc-edit-back"
          @click="onBack"
        />

        <div class="gc-edit-footer-right">
          <q-btn
            flat
            no-caps
            :label="t('dashboard.edit.saveExit')"
            :disable="saving"
            class="gc-edit-save-exit"
            @click="onSaveExit"
          />

          <q-btn
            v-if="currentStep < STEPS.length"
            color="primary"
            unelevated
            no-caps
            icon-right="arrow_forward"
            :label="saving ? t('dashboard.edit.saving') : t('dashboard.edit.next')"
            :loading="saving"
            class="gc-edit-next"
            @click="onNext"
          />

          <q-btn
            v-else
            color="primary"
            unelevated
            no-caps
            icon-right="check"
            :label="t('dashboard.edit.submit')"
            :loading="saving"
            class="gc-edit-next"
            @click="confirmSubmit"
          />
        </div>
      </footer>
    </div>

    <q-dialog v-model="confirmOpen" persistent>
      <q-card class="gc-edit-confirm-card">
        <h3 class="gc-edit-confirm-title">{{ t('dashboard.edit.submitConfirmTitle') }}</h3>
        <p class="gc-edit-confirm-body">{{ t('dashboard.edit.submitConfirmBody') }}</p>
        <div class="gc-edit-confirm-actions">
          <q-btn flat no-caps :label="t('dashboard.edit.submitCancel')" v-close-popup />
          <q-btn
            color="primary"
            unelevated
            no-caps
            :label="t('dashboard.edit.submitConfirmCta')"
            :loading="saving"
            @click="onSubmit"
          />
        </div>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';
import {
  applicationsService,
  type ApplicationDetail,
  type ServiceType,
} from 'src/services/applications';
import { extractApiError } from 'src/utils/api-errors';
import ApplicationStepIndicator from 'src/components/dashboard/ApplicationStepIndicator.vue';

const STEPS = ['service', 'personal', 'details', 'documents', 'review'] as const;

const { t } = useI18n();
const route = useRoute();
const router = useRouter();

const emit = defineEmits<{ 'page-title': [string] }>();

const application = ref<ApplicationDetail | null>(null);
const loading = ref(true);
const saving = ref(false);
const error = ref<string | null>(null);
const submitted = ref(false);
const confirmOpen = ref(false);

const currentStep = computed(() => application.value?.current_step ?? 1);

const headerTitle = computed(() => {
  if (!application.value) return t('dashboard.edit.title');
  return application.value.current_step > 1
    ? t('dashboard.edit.titleEdit')
    : t('dashboard.edit.title');
});

function isValidServiceType(value: unknown): value is ServiceType {
  return value === 'tourism' || value === 'study' || value === 'work' || value === 'visa';
}

async function loadOrCreate() {
  loading.value = true;
  error.value = null;
  try {
    const reference = route.params.reference as string | undefined;

    if (reference) {
      application.value = await applicationsService.detail(reference);
      if (application.value.status !== 'draft') {
        await router.replace(`/dashboard/applications/${reference}`);
      }
    } else {
      const queryType = route.query.type;
      const serviceType: ServiceType = isValidServiceType(queryType) ? queryType : 'study';
      const created = await applicationsService.create({
        service_type: serviceType,
        data: {},
      });
      application.value = created;
      await router.replace(`/dashboard/applications/${created.reference}/edit`);
    }
  } catch (err) {
    application.value = null;
    error.value = extractApiError(err, t('errors.generic'));
  } finally {
    loading.value = false;
  }
}

async function patchApplication(updates: Record<string, unknown>) {
  if (!application.value) return;
  saving.value = true;
  error.value = null;
  try {
    application.value = await applicationsService.update(application.value.reference, updates);
  } catch (err) {
    error.value = extractApiError(err, t('dashboard.edit.saveError'));
    throw err;
  } finally {
    saving.value = false;
  }
}

async function onNext() {
  if (!application.value) return;
  const next = Math.min(application.value.current_step + 1, STEPS.length);
  try {
    await patchApplication({ current_step: next });
  } catch {
    // error already shown
  }
}

async function onBack() {
  if (!application.value) return;
  const prev = Math.max(application.value.current_step - 1, 1);
  try {
    await patchApplication({ current_step: prev });
  } catch {
    // error already shown
  }
}

async function onSaveExit() {
  await router.push('/dashboard/applications');
}

function confirmSubmit() {
  confirmOpen.value = true;
}

async function onSubmit() {
  if (!application.value) return;
  saving.value = true;
  error.value = null;
  try {
    await applicationsService.submit(application.value.reference);
    confirmOpen.value = false;
    submitted.value = true;
  } catch (err) {
    error.value = extractApiError(err, t('errors.generic'));
  } finally {
    saving.value = false;
  }
}

onMounted(async () => {
  emit('page-title', t('dashboard.edit.title'));
  await loadOrCreate();
});

watch(
  () => route.params.reference,
  async (val, oldVal) => {
    if (val !== oldVal) await loadOrCreate();
  },
);
</script>

<style scoped lang="scss">
.gc-edit-loading,
.gc-edit-not-found,
.gc-edit-submitted {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 24px;
  gap: 16px;
  text-align: center;
}

.gc-edit-not-found-title {
  font-size: 22px;
  font-weight: 700;
  margin: 0;
}

.gc-edit-back-btn,
.gc-edit-submitted-btn {
  border-radius: var(--gc-radius-pill);
  padding: 8px 24px;
  font-weight: 600;
}

.gc-edit-submitted-icon {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: rgba(34, 175, 110, 0.14);
  color: #1f9b62;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gc-edit-submitted-title {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-edit-submitted-text {
  color: var(--gc-text-muted);
  margin: 0;
  max-width: 420px;
}

.gc-edit-page {
  display: flex;
  justify-content: center;
}

.gc-edit-shell {
  width: 100%;
  max-width: 880px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  background: var(--gc-bg);
  border: 1px solid var(--gc-border);
  border-radius: var(--gc-radius-lg);
  padding: 24px;

  @media (min-width: 720px) {
    padding: 32px 40px;
  }
}

.gc-edit-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.gc-edit-title {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 28px;
  }
}

.gc-edit-subtitle {
  color: var(--gc-text-muted);
  margin: 0;
  font-size: 14px;
}

.gc-edit-step {
  min-height: 240px;
}

.gc-edit-step-stub {
  background: var(--gc-bg-soft);
  border-radius: var(--gc-radius-md);
  padding: 48px;
  text-align: center;
}

.gc-edit-step-stub-text {
  color: var(--gc-text-muted);
  margin: 0;
}

.gc-edit-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid var(--gc-border);
}

.gc-edit-footer-right {
  display: flex;
  gap: 8px;
}

.gc-edit-back {
  color: var(--gc-text-muted);
}

.gc-edit-save-exit {
  color: var(--gc-text-muted);
}

.gc-edit-next {
  border-radius: var(--gc-radius-pill);
  padding: 8px 20px;
  font-weight: 600;
}

.gc-edit-confirm-card {
  width: 100%;
  max-width: 420px;
  padding: 24px;
  border-radius: var(--gc-radius-lg);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gc-edit-confirm-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-edit-confirm-body {
  font-size: 14px;
  color: var(--gc-text-muted);
  margin: 0;
}

.gc-edit-confirm-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}
</style>
