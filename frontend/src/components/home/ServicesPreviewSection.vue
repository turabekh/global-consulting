<template>
  <section class="gc-services-preview">
    <div class="gc-services-inner">
      <div class="gc-services-card">
        <div class="gc-services-header">
          <h2 class="gc-section-title">
            {{ t('home.services.titlePart1') }}
            <span class="gc-gradient-text">{{ t('home.services.titleHighlight') }}</span>
          </h2>
          <p class="gc-services-subtitle">{{ t('home.services.subtitle') }}</p>
        </div>

        <ul class="gc-service-grid">
          <li v-for="service in services" :key="service.key" class="gc-service-item">
            <div class="gc-service-icon">
              <q-icon :name="service.icon" size="20px" />
            </div>

            <div class="gc-service-text">
              <h3 class="gc-service-title">{{ t(`services.${service.key}.title`) }}</h3>
              <p class="gc-service-desc">{{ t(`services.${service.key}.description`) }}</p>
            </div>

            <q-btn
              :to="service.path"
              color="primary"
              unelevated
              no-caps
              class="gc-service-btn"
              :label="t('services.exploreNow')"
            />
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const services = [
  { key: 'tourism', icon: 'wb_sunny', path: '/services/tourism' },
  { key: 'study', icon: 'menu_book', path: '/services/study' },
  { key: 'work', icon: 'business_center', path: '/services/work' },
  { key: 'visa', icon: 'description', path: '/services/visa' },
] as const;
</script>

<style scoped lang="scss">
.gc-services-preview {
  padding: 32px 16px;

  @media (min-width: 720px) {
    padding: 48px 16px;
  }
}

.gc-services-inner {
  max-width: 1200px;
  margin: 0 auto;
}

.gc-services-card {
  background: var(--gc-bg-soft);
  border-radius: var(--gc-radius-lg);
  padding: 32px 20px;
  display: flex;
  flex-direction: column;
  gap: 32px;

  @media (min-width: 720px) {
    padding: 48px 40px;
    gap: 48px;
  }
}

.gc-services-header {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gc-section-title {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.15;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 36px;
  }
}

.gc-services-subtitle {
  font-size: 14px;
  color: var(--gc-text-muted);
  margin: 0;
  max-width: 480px;
  line-height: 1.5;
}

.gc-service-grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;

  @media (min-width: 600px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (min-width: 1000px) {
    grid-template-columns: repeat(4, 1fr);
  }
}

.gc-service-item {
  background: var(--gc-bg);
  border-radius: var(--gc-radius-md);
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.gc-service-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--gc-primary-soft);
  color: var(--gc-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.gc-service-text {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.gc-service-title {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-service-desc {
  font-size: 13px;
  color: var(--gc-text-muted);
  line-height: 1.45;
  margin: 0;
}

.gc-service-btn {
  align-self: flex-start;
  border-radius: var(--gc-radius-pill);
  padding: 6px 16px;
  font-weight: 500;
  font-size: 13px;
}
</style>
