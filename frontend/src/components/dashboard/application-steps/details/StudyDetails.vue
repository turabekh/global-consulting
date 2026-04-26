<template>
  <div class="gc-form-grid">
    <div class="gc-field gc-field-wide">
      <label class="gc-label" for="study-program">{{
        t('dashboard.edit.detailsStep.study.program')
      }}</label>
      <q-input
        id="study-program"
        v-model="form.program"
        outlined
        dense
        :placeholder="t('dashboard.edit.detailsStep.study.programPlaceholder')"
        @update:model-value="emitChange"
      />
    </div>

    <div class="gc-field">
      <label class="gc-label" for="study-intake-year">{{
        t('dashboard.edit.detailsStep.study.intakeYear')
      }}</label>
      <q-input
        id="study-intake-year"
        v-model.number="form.intake_year"
        outlined
        dense
        type="number"
        :min="currentYear"
        @update:model-value="emitChange"
      />
    </div>

    <div class="gc-field">
      <label class="gc-label" for="study-intake-term">{{
        t('dashboard.edit.detailsStep.study.intakeTerm')
      }}</label>
      <q-select
        id="study-intake-term"
        v-model="form.intake_term"
        :options="termOptions"
        outlined
        dense
        emit-value
        map-options
        @update:model-value="emitChange"
      />
    </div>

    <div class="gc-field gc-field-row">
      <div class="gc-field">
        <label class="gc-label" for="study-budget">{{
          t('dashboard.edit.detailsStep.study.budget')
        }}</label>
        <q-input
          id="study-budget"
          v-model="form.budget"
          outlined
          dense
          type="number"
          min="0"
          @update:model-value="emitChange"
        />
      </div>
      <div class="gc-field gc-field-narrow">
        <label class="gc-label">{{ t('dashboard.edit.detailsStep.study.budgetCurrency') }}</label>
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

    <div class="gc-field">
      <label class="gc-label" for="study-english">{{
        t('dashboard.edit.detailsStep.study.englishLevel')
      }}</label>
      <q-select
        id="study-english"
        v-model="form.english_level"
        :options="englishOptions"
        outlined
        dense
        emit-value
        map-options
        @update:model-value="emitChange"
      />
    </div>

    <div class="gc-field gc-field-wide">
      <label class="gc-label" for="study-prev">{{
        t('dashboard.edit.detailsStep.study.previousEducation')
      }}</label>
      <q-input
        id="study-prev"
        v-model="form.previous_education"
        outlined
        dense
        :placeholder="t('dashboard.edit.detailsStep.study.previousEducationPlaceholder')"
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

interface StudyForm {
  program: string;
  intake_year: number | null;
  intake_term: string;
  budget: string;
  currency: string;
  english_level: string;
  previous_education: string;
}

function pick(source: Record<string, unknown>): StudyForm {
  return {
    program: typeof source.program === 'string' ? source.program : '',
    intake_year: typeof source.intake_year === 'number' ? source.intake_year : null,
    intake_term: typeof source.intake_term === 'string' ? source.intake_term : '',
    budget: typeof source.budget === 'string' ? source.budget : '',
    currency: typeof source.currency === 'string' ? source.currency : 'USD',
    english_level: typeof source.english_level === 'string' ? source.english_level : '',
    previous_education:
      typeof source.previous_education === 'string' ? source.previous_education : '',
  };
}

const form = reactive<StudyForm>(pick(props.data));

const currentYear = new Date().getFullYear();

const termOptions = computed(() => [
  { label: t('dashboard.edit.detailsStep.study.intakeTermOptions.fall'), value: 'fall' },
  { label: t('dashboard.edit.detailsStep.study.intakeTermOptions.spring'), value: 'spring' },
  { label: t('dashboard.edit.detailsStep.study.intakeTermOptions.summer'), value: 'summer' },
]);

const englishOptions = computed(() => [
  { label: t('dashboard.edit.detailsStep.study.englishLevelOptions.basic'), value: 'basic' },
  {
    label: t('dashboard.edit.detailsStep.study.englishLevelOptions.intermediate'),
    value: 'intermediate',
  },
  { label: t('dashboard.edit.detailsStep.study.englishLevelOptions.advanced'), value: 'advanced' },
  { label: t('dashboard.edit.detailsStep.study.englishLevelOptions.native'), value: 'native' },
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
