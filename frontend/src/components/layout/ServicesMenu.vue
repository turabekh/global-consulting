<template>
  <q-menu anchor="bottom middle" self="top middle" :offset="[0, 12]" class="gc-services-menu">
    <div class="gc-services-grid">
      <h3 class="gc-services-title">{{ t('services.exploreTitle') }}</h3>

      <div class="gc-services-cards">
        <router-link
          v-for="service in services"
          :key="service.path"
          :to="service.path"
          class="gc-service-card"
          v-close-popup
        >
          <div class="gc-service-icon">
            <q-icon :name="service.icon" size="20px" />
          </div>
          <div class="gc-service-card-text">
            <span class="gc-service-card-title">{{ t(`services.${service.key}.title`) }}</span>
            <span class="gc-service-card-desc">{{ t(`services.${service.key}.description`) }}</span>
          </div>
        </router-link>
      </div>
    </div>
  </q-menu>
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
.gc-services-menu {
  border-radius: var(--gc-radius-lg);
  box-shadow: 0 12px 48px rgba(15, 15, 15, 0.12);
}

.gc-services-grid {
  padding: 24px;
  width: 480px;
  max-width: 95vw;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.gc-services-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-services-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.gc-service-card {
  display: flex;
  flex-direction: column;
  gap: 28px;
  padding: 16px;
  border-radius: var(--gc-radius-md);
  background: var(--gc-bg-soft);
  text-decoration: none;
  color: var(--gc-text);
  transition:
    background 0.15s ease,
    transform 0.15s ease;

  &:hover {
    background: var(--gc-primary);
    color: #ffffff;

    .gc-service-icon {
      background: rgba(255, 255, 255, 0.2);
      color: #ffffff;
    }

    .gc-service-card-desc {
      color: rgba(255, 255, 255, 0.85);
    }
  }
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
  transition:
    background 0.15s ease,
    color 0.15s ease;
}

.gc-service-card-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.gc-service-card-title {
  font-size: 15px;
  font-weight: 600;
}

.gc-service-card-desc {
  font-size: 12px;
  color: var(--gc-text-muted);
  transition: color 0.15s ease;
  line-height: 1.4;
}
</style>
