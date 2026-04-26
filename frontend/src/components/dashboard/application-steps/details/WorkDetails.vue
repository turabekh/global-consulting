<template>
  <div class="gc-form-grid">
    <div class="gc-field gc-field-wide">
      <label class="gc-label" for="work-role">{{
        t('dashboard.edit.detailsStep.work.currentRole')
      }}</label>
      <q-input
        id="work-role"
        v-model="form.current_role"
        outlined
        dense
        :placeholder="t('dashboard.edit.detailsStep.work.currentRolePlaceholder')"
        @update:model-value="emitChange"
      />
    </div>

    <div class="gc-field">
      <label class="gc-label" for="work-years">{{
        t('dashboard.edit.detailsStep.work.yearsExperience')
      }}</label>
      <q-input
        id="work-years"
        v-model.number="form.years_experience"
        outlined
        dense
        type="number"
        min="0"
        @update:model-value="emitChange"
      />
    </div>

    <div class="gc-field">
      <label class="gc-label" for="work-industry">{{
        t('dashboard.edit.detailsStep.work.targetIndustry')
      }}</label>
      <q-input
        id="work-industry"
        v-model="form.target_industry"
        outlined
        dense
        :placeholder="t('dashboard.edit.detailsStep.work.targetIndustryPlaceholder')"
        @update:model-value="emitChange"
      />
    </div>

    <div class="gc-field">
      <label class="gc-label" for="work-available">{{
        t('dashboard.edit.detailsStep.work.availableFrom')
      }}</label>
      <q-input
        id="work-available"
        v-model="form.available_from"
        outlined
        dense
        type="date"
        @update:model-value="emitChange"
      />
    </div>

    <div class="gc-field gc-field-row">
      <div class="gc-field">
        <label class="gc-label" for="work-salary">{{
          t('dashboard.edit.detailsStep.work.salaryExpectation')
        }}</label>
        <q-input
          id="work-salary"
          v-model="form.salary_expectation"
          outlined
          dense
          type="number"
          min="0"
          @update:model-value="emitChange"
        />
      </div>
      <div class="gc-field gc-field-narrow">
        <label class="gc-label">{{ t('dashboard.edit.detailsStep.work.salaryCurrency') }}</label>
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
      <label class="gc-label">{{ t('dashboard.edit.detailsStep.work.relocationOpen') }}</label>
      <q-option-group
        v-model="form.relocation_open"
        :options="relocationOptions"
        type="radio"
        inline
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

interface WorkForm {
  current_role: string;
  years_experience: number | null;
  target_industry: string;
  available_from: string;
  salary_expectation: string;
  currency: string;
  relocation_open: string;
}

function pick(source: Record<string, unknown>): WorkForm {
  return {
    current_role: typeof source.current_role === 'string' ? source.current_role : '',
    years_experience: typeof source.years_experience === 'number' ? source.years_experience : null,
    target_industry: typeof source.target_industry === 'string' ? source.target_industry : '',
    available_from: typeof source.available_from === 'string' ? source.available_from : '',
    salary_expectation:
      typeof source.salary_expectation === 'string' ? source.salary_expectation : '',
    currency: typeof source.currency === 'string' ? source.currency : 'USD',
    relocation_open: typeof source.relocation_open === 'string' ? source.relocation_open : '',
  };
}

const form = reactive<WorkForm>(pick(props.data));

const relocationOptions = computed(() => [
  { label: t('dashboard.edit.detailsStep.work.yes'), value: 'yes' },
  { label: t('dashboard.edit.detailsStep.work.no'), value: 'no' },
]);

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
