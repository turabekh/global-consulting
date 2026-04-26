<template>
  <div class="gc-step2">
    <header class="gc-step-section-header">
      <h3 class="gc-step-section-title">{{ t('dashboard.edit.personalStep.heading') }}</h3>
      <p class="gc-step-section-sub">{{ t('dashboard.edit.personalStep.subheading') }}</p>
    </header>

    <div class="gc-form-grid">
      <div class="gc-field">
        <label class="gc-label" for="step2-first-name">{{
          t('dashboard.edit.personalStep.firstName')
        }}</label>
        <q-input
          id="step2-first-name"
          v-model="form.first_name"
          outlined
          dense
          :placeholder="t('dashboard.edit.personalStep.firstNamePlaceholder')"
          @update:model-value="emitChange"
        />
      </div>

      <div class="gc-field">
        <label class="gc-label" for="step2-last-name">{{
          t('dashboard.edit.personalStep.lastName')
        }}</label>
        <q-input
          id="step2-last-name"
          v-model="form.last_name"
          outlined
          dense
          :placeholder="t('dashboard.edit.personalStep.lastNamePlaceholder')"
          @update:model-value="emitChange"
        />
      </div>

      <div class="gc-field">
        <label class="gc-label" for="step2-dob">{{
          t('dashboard.edit.personalStep.dateOfBirth')
        }}</label>
        <q-input
          id="step2-dob"
          v-model="form.date_of_birth"
          outlined
          dense
          type="date"
          @update:model-value="emitChange"
        />
      </div>

      <div class="gc-field">
        <label class="gc-label" for="step2-gender">{{
          t('dashboard.edit.personalStep.gender')
        }}</label>
        <q-select
          id="step2-gender"
          v-model="form.gender"
          :options="genderOptions"
          outlined
          dense
          emit-value
          map-options
          @update:model-value="emitChange"
        />
      </div>

      <div class="gc-field">
        <label class="gc-label" for="step2-nationality">{{
          t('dashboard.edit.personalStep.nationality')
        }}</label>
        <q-input
          id="step2-nationality"
          v-model="form.nationality"
          outlined
          dense
          :placeholder="t('dashboard.edit.personalStep.nationalityPlaceholder')"
          @update:model-value="emitChange"
        />
      </div>

      <div class="gc-field">
        <label class="gc-label" for="step2-phone">{{
          t('dashboard.edit.personalStep.phone')
        }}</label>
        <q-input
          id="step2-phone"
          v-model="form.phone"
          outlined
          dense
          :placeholder="t('dashboard.edit.personalStep.phonePlaceholder')"
          @update:model-value="emitChange"
        />
      </div>

      <div class="gc-field">
        <label class="gc-label" for="step2-passport">{{
          t('dashboard.edit.personalStep.passportNumber')
        }}</label>
        <q-input
          id="step2-passport"
          v-model="form.passport_number"
          outlined
          dense
          :placeholder="t('dashboard.edit.personalStep.passportNumberPlaceholder')"
          @update:model-value="emitChange"
        />
      </div>

      <div class="gc-field">
        <label class="gc-label" for="step2-passport-expiry">
          {{ t('dashboard.edit.personalStep.passportExpiry') }}
        </label>
        <q-input
          id="step2-passport-expiry"
          v-model="form.passport_expiry"
          outlined
          dense
          type="date"
          @update:model-value="emitChange"
        />
      </div>

      <div class="gc-field gc-field-wide">
        <label class="gc-label" for="step2-address">{{
          t('dashboard.edit.personalStep.addressLine')
        }}</label>
        <q-input
          id="step2-address"
          v-model="form.address"
          outlined
          dense
          :placeholder="t('dashboard.edit.personalStep.addressPlaceholder')"
          @update:model-value="emitChange"
        />
      </div>

      <div class="gc-field">
        <label class="gc-label" for="step2-city">{{ t('dashboard.edit.personalStep.city') }}</label>
        <q-input
          id="step2-city"
          v-model="form.city"
          outlined
          dense
          @update:model-value="emitChange"
        />
      </div>

      <div class="gc-field">
        <label class="gc-label" for="step2-country">{{
          t('dashboard.edit.personalStep.country')
        }}</label>
        <q-input
          id="step2-country"
          v-model="form.country"
          outlined
          dense
          @update:model-value="emitChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue';
import { useI18n } from 'vue-i18n';

interface Props {
  data: Record<string, unknown>;
}

const props = defineProps<Props>();
const emit = defineEmits<{ 'update:data': [Record<string, unknown>] }>();

const { t } = useI18n();

interface PersonalForm {
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  nationality: string;
  phone: string;
  passport_number: string;
  passport_expiry: string;
  address: string;
  city: string;
  country: string;
}

function pickPersonal(source: Record<string, unknown>): PersonalForm {
  return {
    first_name: typeof source.first_name === 'string' ? source.first_name : '',
    last_name: typeof source.last_name === 'string' ? source.last_name : '',
    date_of_birth: typeof source.date_of_birth === 'string' ? source.date_of_birth : '',
    gender: typeof source.gender === 'string' ? source.gender : '',
    nationality: typeof source.nationality === 'string' ? source.nationality : '',
    phone: typeof source.phone === 'string' ? source.phone : '',
    passport_number: typeof source.passport_number === 'string' ? source.passport_number : '',
    passport_expiry: typeof source.passport_expiry === 'string' ? source.passport_expiry : '',
    address: typeof source.address === 'string' ? source.address : '',
    city: typeof source.city === 'string' ? source.city : '',
    country: typeof source.country === 'string' ? source.country : '',
  };
}

const form = reactive<PersonalForm>(pickPersonal(props.data));

const genderOptions = [
  { label: t('dashboard.edit.personalStep.genderOptions.male'), value: 'male' },
  { label: t('dashboard.edit.personalStep.genderOptions.female'), value: 'female' },
  { label: t('dashboard.edit.personalStep.genderOptions.other'), value: 'other' },
];

let saveTimer: ReturnType<typeof setTimeout> | null = null;

function emitChange() {
  if (saveTimer) clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    emit('update:data', { ...props.data, ...form });
  }, 600);
}

watch(
  () => props.data,
  (next) => {
    Object.assign(form, pickPersonal(next));
  },
);
</script>

<style scoped lang="scss">
.gc-step2 {
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

.gc-form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;

  @media (min-width: 600px) {
    grid-template-columns: 1fr 1fr;
  }
}

.gc-field-wide {
  @media (min-width: 600px) {
    grid-column: span 2;
  }
}
</style>
