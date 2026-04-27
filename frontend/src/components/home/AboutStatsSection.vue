<template>
  <section class="gc-about">
    <div class="gc-about-inner">
      <div v-if="!hideHeading" class="gc-about-header">
        <h2 class="gc-section-title">
          <span class="gc-gradient-text">{{ t('home.about.titlePart1') }}</span>
          {{ t('home.about.titleHighlight') }}
        </h2>
        <p class="gc-section-subtitle">{{ t('home.about.subtitle') }}</p>
      </div>

      <ul class="gc-stats-grid">
        <li v-for="stat in siteConfig.stats" :key="stat.labelKey" class="gc-stat">
          <span class="gc-stat-value">{{ stat.value }}</span>
          <span class="gc-stat-label">{{ t(stat.labelKey) }}</span>
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { siteConfig } from 'src/config/site';

interface Props {
  hideHeading?: boolean;
}

withDefaults(defineProps<Props>(), { hideHeading: false });

const { t } = useI18n();
</script>

<style scoped lang="scss">
.gc-about {
  padding: 48px 16px;
  @media (min-width: 720px) {
    padding: 80px 16px;
  }
}

.gc-about-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 40px;

  @media (min-width: 720px) {
    gap: 64px;
  }
}

.gc-about-header {
  display: flex;
  flex-direction: column;
  gap: 12px;
  text-align: center;
  align-items: center;
}

.gc-section-title {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 40px;
  }
}

.gc-section-subtitle {
  font-size: 15px;
  color: var(--gc-text-muted);
  margin: 0;
  max-width: 540px;
  line-height: 1.5;
}

.gc-stats-grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 32px 24px;
  max-width: 480px;
  margin-left: auto;
  margin-right: auto;

  @media (min-width: 900px) {
    grid-template-columns: repeat(4, 1fr);
    max-width: none;
    gap: 32px;
  }
}

.gc-stat-label {
  font-size: 14px;
  color: var(--gc-text-muted);
  line-height: 1.4;
}

.gc-stat {
  display: flex;
  flex-direction: column;
  gap: 12px;
  text-align: center;
}

.gc-stat-value {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1;
  color: var(--gc-text);

  @media (min-width: 600px) {
    font-size: 40px;
  }

  @media (min-width: 900px) {
    font-size: 56px;
  }
}
</style>
