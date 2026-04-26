<template>
  <div class="gc-step5">
    <header class="gc-step-section-header">
      <h3 class="gc-step-section-title">{{ t('dashboard.edit.reviewStep.heading') }}</h3>
      <p class="gc-step-section-sub">{{ t('dashboard.edit.reviewStep.subheading') }}</p>
    </header>

    <section class="gc-review-section">
      <header class="gc-review-section-header">
        <h4 class="gc-review-section-title">
          {{ t('dashboard.edit.reviewStep.sections.service') }}
        </h4>
        <button
          v-if="!props.readonly"
          type="button"
          class="gc-review-edit"
          @click="emit('go-to-step', 1)"
        >
          {{ t('dashboard.edit.reviewStep.editSection') }}
        </button>
      </header>
      <dl class="gc-review-list">
        <div class="gc-review-row">
          <dt class="gc-review-key">{{ t('dashboard.edit.reviewStep.fields.serviceType') }}</dt>
          <dd class="gc-review-value">{{ serviceLabel }}</dd>
        </div>
        <div class="gc-review-row">
          <dt class="gc-review-key">{{ t('dashboard.edit.reviewStep.fields.target') }}</dt>
          <dd class="gc-review-value">
            {{ application.target_label || t('dashboard.edit.reviewStep.fields.targetEmpty') }}
          </dd>
        </div>
      </dl>
    </section>

    <section class="gc-review-section">
      <header class="gc-review-section-header">
        <h4 class="gc-review-section-title">
          {{ t('dashboard.edit.reviewStep.sections.personal') }}
        </h4>
        <button
          v-if="!props.readonly"
          type="button"
          class="gc-review-edit"
          @click="emit('go-to-step', 2)"
        >
          {{ t('dashboard.edit.reviewStep.editSection') }}
        </button>
      </header>
      <dl class="gc-review-list">
        <div v-for="row in personalRows" :key="row.key" class="gc-review-row">
          <dt class="gc-review-key">{{ row.label }}</dt>
          <dd class="gc-review-value">{{ row.value }}</dd>
        </div>
      </dl>
    </section>

    <section class="gc-review-section">
      <header class="gc-review-section-header">
        <h4 class="gc-review-section-title">
          {{ t('dashboard.edit.reviewStep.sections.details') }}
        </h4>
        <button
          v-if="!props.readonly"
          type="button"
          class="gc-review-edit"
          @click="emit('go-to-step', 3)"
        >
          {{ t('dashboard.edit.reviewStep.editSection') }}
        </button>
      </header>
      <dl class="gc-review-list">
        <div v-for="row in detailsRows" :key="row.key" class="gc-review-row">
          <dt class="gc-review-key">{{ row.label }}</dt>
          <dd class="gc-review-value">{{ row.value }}</dd>
        </div>
      </dl>
    </section>

    <section class="gc-review-section">
      <header class="gc-review-section-header">
        <h4 class="gc-review-section-title">
          {{ t('dashboard.edit.reviewStep.sections.documents') }}
        </h4>
        <button
          v-if="!props.readonly"
          type="button"
          class="gc-review-edit"
          @click="emit('go-to-step', 4)"
        >
          {{ t('dashboard.edit.reviewStep.editSection') }}
        </button>
      </header>

      <p v-if="application.documents.length === 0" class="gc-review-empty">
        {{ t('dashboard.edit.reviewStep.noDocuments') }}
      </p>

      <ul v-else class="gc-review-docs">
        <li v-for="doc in application.documents" :key="doc.id" class="gc-review-doc">
          <q-icon name="description" size="16px" />
          <span>{{ doc.original_filename }}</span>
          <span class="gc-review-doc-kind">{{ kindLabel(doc.kind) }}</span>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import type { ApplicationDetail, DocumentKind } from 'src/services/applications';

interface Props {
  application: ApplicationDetail;
  readonly?: boolean;
}

const props = withDefaults(defineProps<Props>(), { readonly: false });
const emit = defineEmits<{ 'go-to-step': [number] }>();

const { t } = useI18n();

interface Row {
  key: string;
  label: string;
  value: string;
}

const missing = computed(() => t('dashboard.edit.reviewStep.missingValue'));

function show(value: unknown): string {
  if (value === null || value === undefined || value === '') return missing.value;
  if (typeof value === 'string') return value;
  if (typeof value === 'number' || typeof value === 'boolean') return String(value);
  return missing.value;
}

function showAmount(amount: unknown, currency: unknown): string {
  if (amount === null || amount === undefined || amount === '') return missing.value;
  if (typeof amount !== 'string' && typeof amount !== 'number') return missing.value;
  const c = typeof currency === 'string' ? currency : '';
  return c ? `${amount} ${c}` : String(amount);
}

function showOption(value: unknown, path: string): string {
  if (value === null || value === undefined || value === '') return missing.value;
  if (typeof value !== 'string') return missing.value;
  return t(`${path}.${value}`);
}

function showBool(value: unknown): string {
  if (value === 'yes') return t('dashboard.edit.detailsStep.work.yes');
  if (value === 'no') return t('dashboard.edit.detailsStep.work.no');
  return missing.value;
}

const serviceLabel = computed(() =>
  t(`dashboard.overview.serviceLabels.${props.application.service_type}`),
);

const personalRows = computed<Row[]>(() => {
  const d = props.application.data;
  return [
    {
      key: 'first_name',
      label: t('dashboard.edit.reviewStep.fields.firstName'),
      value: show(d.first_name),
    },
    {
      key: 'last_name',
      label: t('dashboard.edit.reviewStep.fields.lastName'),
      value: show(d.last_name),
    },
    {
      key: 'date_of_birth',
      label: t('dashboard.edit.reviewStep.fields.dateOfBirth'),
      value: show(d.date_of_birth),
    },
    {
      key: 'gender',
      label: t('dashboard.edit.reviewStep.fields.gender'),
      value: showOption(d.gender, 'dashboard.edit.personalStep.genderOptions'),
    },
    {
      key: 'nationality',
      label: t('dashboard.edit.reviewStep.fields.nationality'),
      value: show(d.nationality),
    },
    { key: 'phone', label: t('dashboard.edit.reviewStep.fields.phone'), value: show(d.phone) },
    {
      key: 'passport_number',
      label: t('dashboard.edit.reviewStep.fields.passportNumber'),
      value: show(d.passport_number),
    },
    {
      key: 'passport_expiry',
      label: t('dashboard.edit.reviewStep.fields.passportExpiry'),
      value: show(d.passport_expiry),
    },
    {
      key: 'address',
      label: t('dashboard.edit.reviewStep.fields.address'),
      value: show(d.address),
    },
    { key: 'city', label: t('dashboard.edit.reviewStep.fields.city'), value: show(d.city) },
    {
      key: 'country',
      label: t('dashboard.edit.reviewStep.fields.country'),
      value: show(d.country),
    },
  ];
});

const detailsRows = computed<Row[]>(() => {
  const d = props.application.data;
  const type = props.application.service_type;

  if (type === 'tourism') {
    return [
      {
        key: 'travel_start',
        label: t('dashboard.edit.reviewStep.fields.travelStart'),
        value: show(d.travel_start),
      },
      {
        key: 'travel_end',
        label: t('dashboard.edit.reviewStep.fields.travelEnd'),
        value: show(d.travel_end),
      },
      {
        key: 'travelers',
        label: t('dashboard.edit.reviewStep.fields.travelers'),
        value: show(d.travelers),
      },
      {
        key: 'budget',
        label: t('dashboard.edit.reviewStep.fields.budget'),
        value: showAmount(d.budget, d.currency),
      },
      {
        key: 'preferences',
        label: t('dashboard.edit.reviewStep.fields.preferences'),
        value: show(d.preferences),
      },
    ];
  }

  if (type === 'study') {
    return [
      {
        key: 'program',
        label: t('dashboard.edit.reviewStep.fields.program'),
        value: show(d.program),
      },
      {
        key: 'intake_year',
        label: t('dashboard.edit.reviewStep.fields.intakeYear'),
        value: show(d.intake_year),
      },
      {
        key: 'intake_term',
        label: t('dashboard.edit.reviewStep.fields.intakeTerm'),
        value: showOption(d.intake_term, 'dashboard.edit.detailsStep.study.intakeTermOptions'),
      },
      {
        key: 'budget',
        label: t('dashboard.edit.reviewStep.fields.budget'),
        value: showAmount(d.budget, d.currency),
      },
      {
        key: 'english_level',
        label: t('dashboard.edit.reviewStep.fields.englishLevel'),
        value: showOption(d.english_level, 'dashboard.edit.detailsStep.study.englishLevelOptions'),
      },
      {
        key: 'previous_education',
        label: t('dashboard.edit.reviewStep.fields.previousEducation'),
        value: show(d.previous_education),
      },
    ];
  }

  if (type === 'work') {
    return [
      {
        key: 'current_role',
        label: t('dashboard.edit.reviewStep.fields.currentRole'),
        value: show(d.current_role),
      },
      {
        key: 'years_experience',
        label: t('dashboard.edit.reviewStep.fields.yearsExperience'),
        value: show(d.years_experience),
      },
      {
        key: 'target_industry',
        label: t('dashboard.edit.reviewStep.fields.targetIndustry'),
        value: show(d.target_industry),
      },
      {
        key: 'available_from',
        label: t('dashboard.edit.reviewStep.fields.availableFrom'),
        value: show(d.available_from),
      },
      {
        key: 'salary_expectation',
        label: t('dashboard.edit.reviewStep.fields.salaryExpectation'),
        value: showAmount(d.salary_expectation, d.currency),
      },
      {
        key: 'relocation_open',
        label: t('dashboard.edit.reviewStep.fields.relocationOpen'),
        value: showBool(d.relocation_open),
      },
    ];
  }

  if (type === 'visa') {
    return [
      {
        key: 'target_country',
        label: t('dashboard.edit.reviewStep.fields.targetCountry'),
        value: show(d.target_country),
      },
      {
        key: 'visa_category',
        label: t('dashboard.edit.reviewStep.fields.visaCategory'),
        value: showOption(d.visa_category, 'dashboard.edit.detailsStep.visa.visaCategoryOptions'),
      },
      {
        key: 'intended_duration',
        label: t('dashboard.edit.reviewStep.fields.intendedDuration'),
        value: show(d.intended_duration),
      },
      {
        key: 'previous_visas',
        label: t('dashboard.edit.reviewStep.fields.previousVisas'),
        value: show(d.previous_visas),
      },
    ];
  }

  return [];
});

function kindLabel(kind: DocumentKind): string {
  return t(`dashboard.edit.documentsStep.kinds.${kind}`);
}
</script>

<style scoped lang="scss">
.gc-step5 {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.gc-step-section-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.gc-step-section-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-step-section-sub {
  font-size: 13px;
  color: var(--gc-text-muted);
  margin: 0;
}

.gc-review-section {
  background: var(--gc-bg-soft);
  border-radius: var(--gc-radius-md);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gc-review-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.gc-review-section-title {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  color: var(--gc-text-muted);
  margin: 0;
}

.gc-review-edit {
  appearance: none;
  border: none;
  background: transparent;
  color: var(--gc-primary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: var(--gc-radius-pill);

  &:hover {
    background: var(--gc-primary-soft);
  }
}

.gc-review-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
  margin: 0;

  @media (min-width: 600px) {
    grid-template-columns: 1fr 1fr;
    gap: 12px 24px;
  }
}

.gc-review-row {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.gc-review-key {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gc-text-muted);
  font-weight: 600;
}

.gc-review-value {
  font-size: 14px;
  color: var(--gc-text);
  margin: 0;
  word-break: break-word;
}

.gc-review-empty {
  font-size: 13px;
  color: var(--gc-text-muted);
  margin: 0;
}

.gc-review-docs {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.gc-review-doc {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: var(--gc-radius-sm);
  background: var(--gc-bg);
  font-size: 13px;
}

.gc-review-doc-kind {
  margin-left: auto;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gc-text-muted);
  font-weight: 600;
}
</style>
