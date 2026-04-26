<template>
  <div v-if="!submitted" class="gc-partnership-form-root">
    <q-form class="gc-form-body" @submit.prevent="onSubmit">
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
  </div>

  <AuthSuccessCard
    v-else
    icon="check"
    :title="t('forms.partnership.successTitle')"
    :message="t('forms.partnership.successMessage')"
    :action-label="t('forms.partnership.successAction')"
    @action="onDone"
  />
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { inquiriesService } from 'src/services/inquiries';
import { extractApiError } from 'src/utils/api-errors';
import AuthSuccessCard from 'src/components/AuthSuccessCard.vue';

interface Props {
  resetSignal?: number;
}

const props = defineProps<Props>();
const emit = defineEmits<{ done: [] }>();

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

watch(
  () => props.resetSignal,
  () => reset(),
);

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

function onDone() {
  emit('done');
}
</script>

<style scoped lang="scss">
.gc-partnership-form-root {
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
