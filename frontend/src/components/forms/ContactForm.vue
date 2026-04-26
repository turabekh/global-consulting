<template>
  <div v-if="!submitted" class="gc-contact-form-root">
    <q-form class="gc-form-body" @submit.prevent="onSubmit">
      <div class="gc-field">
        <label class="gc-label" for="contact-name">{{ t('forms.contact.fullName') }}</label>
        <q-input
          id="contact-name"
          v-model="fullName"
          outlined
          dense
          :placeholder="t('forms.contact.fullNamePlaceholder')"
          :rules="[(v) => !!v || t('errors.required')]"
          lazy-rules
        />
      </div>

      <div class="gc-field">
        <label class="gc-label" for="contact-info">{{ t('forms.contact.contact') }}</label>
        <q-input
          id="contact-info"
          v-model="contact"
          outlined
          dense
          :placeholder="t('forms.contact.contactPlaceholder')"
          :rules="[(v) => !!v || t('errors.required')]"
          lazy-rules
        />
      </div>

      <div class="gc-field">
        <label class="gc-label" for="contact-service">{{ t('forms.contact.serviceType') }}</label>
        <q-select
          id="contact-service"
          v-model="serviceType"
          :options="serviceOptions"
          outlined
          dense
          emit-value
          map-options
          :placeholder="t('forms.contact.serviceTypeSelect')"
        />
      </div>

      <div class="gc-field">
        <label class="gc-label" for="contact-note">{{ t('forms.contact.note') }}</label>
        <q-input
          id="contact-note"
          v-model="note"
          outlined
          type="textarea"
          autogrow
          :placeholder="t('forms.contact.notePlaceholder')"
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
        :label="t('forms.contact.submit')"
      />
    </q-form>
  </div>

  <AuthSuccessCard
    v-else
    icon="check"
    :title="t('forms.contact.successTitle')"
    :message="t('forms.contact.successMessage')"
    :action-label="t('forms.contact.successAction')"
    @action="onDone"
  />
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { inquiriesService, type ServiceType } from 'src/services/inquiries';
import { extractApiError } from 'src/utils/api-errors';
import AuthSuccessCard from 'src/components/AuthSuccessCard.vue';

interface Props {
  resetSignal?: number;
}

const props = defineProps<Props>();
const emit = defineEmits<{ done: [] }>();

const { t } = useI18n();

const fullName = ref('');
const contact = ref('');
const serviceType = ref<ServiceType>('other');
const note = ref('');
const loading = ref(false);
const error = ref<string | null>(null);
const submitted = ref(false);

const serviceOptions = [
  { label: t('forms.serviceTypes.tourism'), value: 'tourism' },
  { label: t('forms.serviceTypes.study'), value: 'study' },
  { label: t('forms.serviceTypes.work'), value: 'work' },
  { label: t('forms.serviceTypes.visa'), value: 'visa' },
  { label: t('forms.serviceTypes.other'), value: 'other' },
];

function reset() {
  fullName.value = '';
  contact.value = '';
  serviceType.value = 'other';
  note.value = '';
  error.value = null;
  submitted.value = false;
}

watch(
  () => props.resetSignal,
  () => reset(),
);

async function onSubmit() {
  error.value = null;
  loading.value = true;
  try {
    await inquiriesService.submitContact({
      full_name: fullName.value,
      contact: contact.value,
      service_type: serviceType.value,
      note: note.value,
    });
    submitted.value = true;
  } catch (err) {
    error.value = extractApiError(err, t('errors.generic'));
  } finally {
    loading.value = false;
  }
}

function onDone() {
  emit('done');
}
</script>

<style scoped lang="scss">
.gc-contact-form-root {
  display: contents;
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
