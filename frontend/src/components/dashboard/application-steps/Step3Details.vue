<template>
  <div class="gc-step3">
    <header class="gc-step-section-header">
      <h3 class="gc-step-section-title">{{ t('dashboard.edit.detailsStep.heading') }}</h3>
      <p class="gc-step-section-sub">{{ t('dashboard.edit.detailsStep.subheading') }}</p>
    </header>

    <component
      :is="activeComponent"
      :data="data"
      @update:data="(value) => emit('update:data', value)"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import TourismDetails from './details/TourismDetails.vue';
import StudyDetails from './details/StudyDetails.vue';
import WorkDetails from './details/WorkDetails.vue';
import VisaDetails from './details/VisaDetails.vue';
import type { ServiceType } from 'src/services/applications';

interface Props {
  serviceType: ServiceType;
  data: Record<string, unknown>;
}

const props = defineProps<Props>();
const emit = defineEmits<{ 'update:data': [Record<string, unknown>] }>();

const { t } = useI18n();

const activeComponent = computed(() => {
  switch (props.serviceType) {
    case 'tourism':
      return TourismDetails;
    case 'study':
      return StudyDetails;
    case 'work':
      return WorkDetails;
    case 'visa':
      return VisaDetails;
    default:
      return TourismDetails;
  }
});
</script>

<style scoped lang="scss">
.gc-step3 {
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
</style>
