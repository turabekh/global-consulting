<template>
  <div class="gc-success-card">
    <div class="gc-success-icon">
      <q-icon :name="icon" size="32px" />
    </div>
    <h2 class="gc-success-title">{{ title }}</h2>
    <p class="gc-success-message">{{ message }}</p>
    <q-btn
      v-if="actionLabel"
      color="primary"
      unelevated
      no-caps
      class="gc-success-btn full-width"
      :label="actionLabel"
      @click="emit('action')"
    />
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    title: string;
    message: string;
    icon?: string;
    actionLabel?: string;
  }>(),
  { icon: 'check' },
);

const emit = defineEmits<{ action: [] }>();
</script>

<style scoped lang="scss">
.gc-success-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 16px;
  padding: 24px 0;
}

.gc-success-icon {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: var(--gc-primary-soft);
  color: var(--gc-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.gc-success-title {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-success-message {
  color: var(--gc-text-muted);
  font-size: 14px;
  margin: 0;
  max-width: 320px;
  line-height: 1.5;
}

.gc-success-btn {
  border-radius: var(--gc-radius-pill);
  font-weight: 600;
  padding: 8px 0;
  margin-top: 8px;
}
</style>
