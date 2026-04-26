<template>
  <div class="gc-dash-stub">
    <h2>Dashboard overview coming next</h2>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const emit = defineEmits<{ 'page-title': [string] }>();

onMounted(() => {
  emit('page-title', t('dashboard.overview.title'));
});
</script>

<style scoped lang="scss">
.gc-dash-stub {
  background: var(--gc-bg);
  border-radius: var(--gc-radius-lg);
  padding: 48px;
  text-align: center;
  color: var(--gc-text-muted);
}
</style>
