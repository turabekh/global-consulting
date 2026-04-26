<template>
  <span class="gc-status-badge" :class="`gc-status-${status}`">
    <span class="gc-status-dot" aria-hidden="true"></span>
    {{ t(`dashboard.overview.statusLabels.${status}`) }}
  </span>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import type { ApplicationStatus } from 'src/services/applications';

defineProps<{ status: ApplicationStatus }>();

const { t } = useI18n();
</script>

<style scoped lang="scss">
.gc-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: var(--gc-radius-pill);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.gc-status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.gc-status-draft {
  background: rgba(150, 150, 150, 0.12);
  color: #666;
}

.gc-status-submitted,
.gc-status-in_review {
  background: rgba(74, 141, 255, 0.12);
  color: #4a8dff;
}

.gc-status-needs_info {
  background: rgba(255, 178, 50, 0.16);
  color: #c97900;
}

.gc-status-accepted {
  background: rgba(34, 175, 110, 0.14);
  color: #1f9b62;
}

.gc-status-rejected,
.gc-status-closed {
  background: rgba(255, 99, 99, 0.14);
  color: #d04848;
}
</style>
