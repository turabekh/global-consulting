<template>
  <q-dialog v-model="open" persistent>
    <q-card class="gc-form-card">
      <header v-if="!submitted" class="gc-form-header">
        <div class="gc-form-header-text">
          <h2 class="gc-form-title">{{ t('forms.partnership.title') }}</h2>
          <p class="gc-form-subtitle">{{ t('forms.partnership.subtitle') }}</p>
        </div>
        <q-btn flat round dense icon="close" v-close-popup aria-label="Close" />
      </header>

      <q-form v-if="!submitted" class="gc-form-body" @submit.prevent="onSubmit">
        <div class="gc-field">
          <label class="gc-label" for="partnership-company">{{
            t('forms.partnership.companyName')
          }}</label>
          <q-input
            id="partnership-company"
            v-model="companyName"
            outlined
            dense
            :placeholder="t('forms.partnership.companyNamePlaceholder')"
            :rules="[(v) => !!v || t('errors.required')]"
            lazy-rules
          />
        </div>

        <div class="gc-field">
          <label class="gc-label" for="partnership-contact">{{
            t('forms.partnership.contact')
          }}</label>
          <q-input
            id="partnership-contact"
            v-model="contact"
            outlined
            dense
            :placeholder="t('forms.partnership.contactPlaceholder')"
            :rules="[(v) => !!v || t('errors.required')]"
            lazy-rules
          />
        </div>

        <div class="gc-field">
          <label class="gc-label" for="partnership-goals">{{ t('forms.partnership.goals') }}</label>
          <q-input
            id="partnership-goals"
            v-model="goals"
            outlined
            type="textarea"
            autogrow
            :placeholder="t('forms.partnership.goalsPlaceholder')"
            :rules="[(v) => !!v || t('errors.required')]"
            lazy-rules
          />
        </div>

        <q-banner v-if="error" class="gc-error-banner" dense rounded>{{ error }}</q-banner>

        <q-btn
          type="submit"
          color="primary"
          unelevated
          no-caps
          size="md"
          :loading="loading"
          class="gc-submit-btn full-width"
          :label="t('forms.partnership.submit')"
        />
      </q-form>

      <AuthSuccessCard
        v-else
        icon="check"
        :title="t('forms.partnership.successTitle')"
        :message="t('forms.partnership.successMessage')"
        :action-label="t('forms.partnership.successAction')"
        @action="onClose"
      />
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { inquiriesService } from 'src/services/inquiries';
import { extractApiError } from 'src/utils/api-errors';
import AuthSuccessCard from 'src/components/AuthSuccessCard.vue';

const open = defineModel<boolean>({ required: true });

const { t } = useI18n();

const companyName = ref('');
const contact = ref('');
const goals = ref('');
const loading = ref(false);
const error = ref<string | null>(null);
const submitted = ref(false);

function reset() {
  companyName.value = '';
  contact.value = '';
  goals.value = '';
  error.value = null;
  submitted.value = false;
}

watch(open, (v) => {
  if (v) reset();
});

async function onSubmit() {
  error.value = null;
  loading.value = true;
  try {
    await inquiriesService.submitPartnership({
      company_name: companyName.value,
      contact: contact.value,
      goals: goals.value,
    });
    submitted.value = true;
  } catch (err) {
    error.value = extractApiError(err, t('errors.generic'));
  } finally {
    loading.value = false;
  }
}

function onClose() {
  open.value = false;
}
</script>

<style scoped lang="scss">
.gc-form-card {
  width: 100%;
  max-width: 440px;
  border-radius: var(--gc-radius-lg);
  padding: 24px;
}

.gc-form-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 20px;
}

.gc-form-header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.gc-form-title {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-form-subtitle {
  font-size: 13px;
  color: var(--gc-text-muted);
  margin: 0;
}

.gc-form-body {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.gc-submit-btn {
  border-radius: var(--gc-radius-pill);
  font-weight: 600;
  padding: 8px 0;
  margin-top: 4px;
}
</style>
