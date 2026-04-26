<template>
  <div class="gc-step-indicator">
    <span class="gc-step-counter">
      {{ t('dashboard.edit.stepLabel', { current, total }) }}
    </span>
    <ol class="gc-step-list" :aria-label="t('dashboard.edit.title')">
      <li
        v-for="(step, idx) in steps"
        :key="step"
        class="gc-step-item"
        :class="{
          'gc-step-item-current': idx + 1 === current,
          'gc-step-item-done': idx + 1 < current,
        }"
      >
        <span class="gc-step-dot">
          <q-icon v-if="idx + 1 < current" name="check" size="14px" />
          <span v-else>{{ idx + 1 }}</span>
        </span>
        <span class="gc-step-label">
          {{ t(`dashboard.edit.steps.${step}`) }}
        </span>
      </li>
    </ol>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

interface Props {
  current: number;
  steps: readonly string[];
}

const props = defineProps<Props>();

const { t } = useI18n();

const total = computed(() => props.steps.length);
</script>

<style scoped lang="scss">
.gc-step-indicator {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gc-step-counter {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gc-text-muted);
  font-weight: 600;
}

.gc-step-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: center;
}

.gc-step-item {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--gc-text-muted);
  position: relative;

  &::after {
    content: '';
    width: 24px;
    height: 1px;
    background: var(--gc-border);
    margin-left: 8px;
    display: none;

    @media (min-width: 720px) {
      display: inline-block;
    }
  }

  &:last-child::after {
    display: none;
  }
}

.gc-step-dot {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--gc-bg-soft);
  border: 1px solid var(--gc-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  color: var(--gc-text-muted);
  flex-shrink: 0;
}

.gc-step-item-current {
  color: var(--gc-text);
  font-weight: 600;

  .gc-step-dot {
    background: var(--gc-primary);
    border-color: var(--gc-primary);
    color: #ffffff;
  }
}

.gc-step-item-done {
  color: var(--gc-text-muted);

  .gc-step-dot {
    background: var(--gc-primary-soft);
    border-color: var(--gc-primary);
    color: var(--gc-primary);
  }
}

.gc-step-label {
  display: none;

  @media (min-width: 600px) {
    display: inline;
  }
}
</style>
