<template>
  <div class="gc-form-grid">
    <div class="gc-field">
      <label class="gc-label" for="visa-country">{{
        t('dashboard.edit.detailsStep.visa.targetCountry')
      }}</label>
      <q-input
        id="visa-country"
        v-model="form.target_country"
        outlined
        dense
        :placeholder="t('dashboard.edit.detailsStep.visa.targetCountryPlaceholder')"
        @update:model-value="emitChange"
      />
    </div>

    <div class="gc-field">
      <label class="gc-label" for="visa-category">{{
        t('dashboard.edit.detailsStep.visa.visaCategory')
      }}</label>
      <q-select
        id="visa-category"
        v-model="form.visa_category"
        :options="categoryOptions"
        outlined
        dense
        emit-value
        map-options
        @update:model-value="emitChange"
      />
    </div>

    <div class="gc-field gc-field-wide">
      <label class="gc-label" for="visa-duration">{{
        t('dashboard.edit.detailsStep.visa.intendedDuration')
      }}</label>
      <q-input
        id="visa-duration"
        v-model="form.intended_duration"
        outlined
        dense
        :placeholder="t('dashboard.edit.detailsStep.visa.intendedDurationPlaceholder')"
        @update:model-value="emitChange"
      />
    </div>

    <div class="gc-field gc-field-wide">
      <label class="gc-label" for="visa-history">{{
        t('dashboard.edit.detailsStep.visa.previousVisas')
      }}</label>
      <q-input
        id="visa-history"
        v-model="form.previous_visas"
        outlined
        dense
        type="textarea"
        autogrow
        :placeholder="t('dashboard.edit.detailsStep.visa.previousVisasPlaceholder')"
        @update:model-value="emitChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { debouncedEmit } from 'src/utils/debounced-emit';

interface Props {
  data: Record<string, unknown>;
}

const props = defineProps<Props>();
const emit = defineEmits<{ 'update:data': [Record<string, unknown>] }>();

const { t } = useI18n();

interface VisaForm {
  target_country: string;
  visa_category: string;
  intended_duration: string;
  previous_visas: string;
}

function pick(source: Record<string, unknown>): VisaForm {
  return {
    target_country: typeof source.target_country === 'string' ? source.target_country : '',
    visa_category: typeof source.visa_category === 'string' ? source.visa_category : '',
    intended_duration: typeof source.intended_duration === 'string' ? source.intended_duration : '',
    previous_visas: typeof source.previous_visas === 'string' ? source.previous_visas : '',
  };
}

const form = reactive<VisaForm>(pick(props.data));

const categoryOptions = computed(() => [
  { label: t('dashboard.edit.detailsStep.visa.visaCategoryOptions.tourist'), value: 'tourist' },
  { label: t('dashboard.edit.detailsStep.visa.visaCategoryOptions.student'), value: 'student' },
  { label: t('dashboard.edit.detailsStep.visa.visaCategoryOptions.work'), value: 'work' },
  { label: t('dashboard.edit.detailsStep.visa.visaCategoryOptions.business'), value: 'business' },
  { label: t('dashboard.edit.detailsStep.visa.visaCategoryOptions.family'), value: 'family' },
]);

const debouncedFire = debouncedEmit((payload: Record<string, unknown>) => {
  emit('update:data', payload);
});

function emitChange() {
  debouncedFire({ ...props.data, ...form });
}

watch(
  () => props.data,
  (next) => {
    Object.assign(form, pick(next));
  },
);
</script>

<style scoped lang="scss">
@import '../shared-step.scss';
</style>
