<template>
  <q-dialog v-model="open" persistent>
    <q-card class="gc-form-card">
      <header class="gc-form-header">
        <div class="gc-form-header-text">
          <h2 class="gc-form-title">{{ t('forms.partnership.title') }}</h2>
          <p class="gc-form-subtitle">{{ t('forms.partnership.subtitle') }}</p>
        </div>
        <q-btn flat round dense icon="close" v-close-popup aria-label="Close" />
      </header>

      <PartnershipForm :reset-signal="resetSignal" @done="onDone" />
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import PartnershipForm from './PartnershipForm.vue';

const open = defineModel<boolean>({ required: true });

const { t } = useI18n();
const resetSignal = ref(0);

watch(open, (v) => {
  if (v) resetSignal.value++;
});

function onDone() {
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
</style>
