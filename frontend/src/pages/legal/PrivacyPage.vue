<template>
  <q-page class="gc-legal-page">
    <div class="gc-legal-shell">
      <h1 class="gc-h1">{{ t('legal.privacyTitle') }}</h1>
      <p class="gc-subtitle">{{ t('legal.comingSoon') }}</p>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>

<style scoped lang="scss">
.gc-legal-page {
  background: var(--gc-bg);
  min-height: calc(100vh - 64px);
  padding: 64px 16px;
}

.gc-legal-shell {
  max-width: 720px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>
