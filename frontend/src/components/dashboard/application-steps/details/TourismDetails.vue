<template>
  <div class="gc-form-grid">
    <div class="gc-field">
      <label class="gc-label" for="tourism-start">{{
        t('dashboard.edit.detailsStep.tourism.travelStart')
      }}</label>
      <q-input
        id="tourism-start"
        v-model="form.travel_start"
        outlined
        dense
        type="date"
        @update:model-value="emitChange"
      />
    </div>

    <div class="gc-field">
      <label class="gc-label" for="tourism-end">{{
        t('dashboard.edit.detailsStep.tourism.travelEnd')
      }}</label>
      <q-input
        id="tourism-end"
        v-model="form.travel_end"
        outlined
        dense
        type="date"
        @update:model-value="emitChange"
      />
    </div>

    <div class="gc-field">
      <label class="gc-label" for="tourism-travelers">{{
        t('dashboard.edit.detailsStep.tourism.travelers')
      }}</label>
      <q-input
        id="tourism-travelers"
        v-model.number="form.travelers"
        outlined
        dense
        type="number"
        min="1"
        @update:model-value="emitChange"
      />
    </div>

    <div class="gc-field gc-field-row">
      <div class="gc-field">
        <label class="gc-label" for="tourism-budget">{{
          t('dashboard.edit.detailsStep.tourism.budget')
        }}</label>
        <q-input
          id="tourism-budget"
          v-model="form.budget"
          outlined
          dense
          type="number"
          min="0"
          @update:model-value="emitChange"
        />
      </div>
      <div class="gc-field gc-field-narrow">
        <label class="gc-label">{{ t('dashboard.edit.detailsStep.tourism.budgetCurrency') }}</label>
        <q-select
          v-model="form.currency"
          :options="currencyOptions"
          outlined
          dense
          emit-value
          map-options
          @update:model-value="emitChange"
        />
      </div>
    </div>

    <div class="gc-field gc-field-wide">
      <label class="gc-label" for="tourism-prefs">{{
        t('dashboard.edit.detailsStep.tourism.preferences')
      }}</label>
      <q-input
        id="tourism-prefs"
        v-model="form.preferences"
        outlined
        dense
        type="textarea"
        autogrow
        :placeholder="t('dashboard.edit.detailsStep.tourism.preferencesPlaceholder')"
        @update:model-value="emitChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { debouncedEmit } from 'src/utils/debounced-emit';

interface Props {
  data: Record<string, unknown>;
}

const props = defineProps<Props>();
const emit = defineEmits<{ 'update:data': [Record<string, unknown>] }>();

const { t } = useI18n();

interface TourismForm {
  travel_start: string;
  travel_end: string;
  travelers: number | null;
  budget: string;
  currency: string;
  preferences: string;
}

function pick(source: Record<string, unknown>): TourismForm {
  return {
    travel_start: typeof source.travel_start === 'string' ? source.travel_start : '',
    travel_end: typeof source.travel_end === 'string' ? source.travel_end : '',
    travelers: typeof source.travelers === 'number' ? source.travelers : null,
    budget: typeof source.budget === 'string' ? source.budget : '',
    currency: typeof source.currency === 'string' ? source.currency : 'USD',
    preferences: typeof source.preferences === 'string' ? source.preferences : '',
  };
}

const form = reactive<TourismForm>(pick(props.data));

const currencyOptions = [
  { label: 'USD', value: 'USD' },
  { label: 'EUR', value: 'EUR' },
  { label: 'UZS', value: 'UZS' },
];

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
