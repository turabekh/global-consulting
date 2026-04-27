<template>
  <q-page class="gc-partnership-page">
    <div class="gc-partnership-shell">
      <header class="gc-partnership-header">
        <h1 class="gc-partnership-title">
          {{ t('pages.partnership.title') }}
          <span class="gc-gradient-text">{{ t('pages.partnership.titleHighlight') }}</span>
        </h1>
        <p class="gc-partnership-subtitle">{{ t('pages.partnership.subtitle') }}</p>
      </header>

      <div class="gc-partnership-grid">
        <aside class="gc-partnership-info">
          <h2 class="gc-info-heading">{{ t('pages.partnership.benefitsTitle') }}</h2>

          <ul class="gc-benefits-list">
            <li v-for="benefit in benefits" :key="benefit.key" class="gc-benefit-item">
              <div class="gc-benefit-icon">
                <q-icon :name="benefit.icon" size="22px" />
              </div>
              <div class="gc-benefit-text">
                <span class="gc-benefit-title">
                  {{ t(`pages.partnership.benefits.${benefit.key}.title`) }}
                </span>
                <span class="gc-benefit-desc">
                  {{ t(`pages.partnership.benefits.${benefit.key}.description`) }}
                </span>
              </div>
            </li>
          </ul>
        </aside>

        <div class="gc-partnership-form-wrap">
          <header class="gc-form-card-header">
            <h2 class="gc-form-card-title">{{ t('forms.partnership.title') }}</h2>
            <p class="gc-form-card-subtitle">{{ t('forms.partnership.subtitle') }}</p>
          </header>

          <PartnershipForm @done="onDone" />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import PartnershipForm from 'src/components/forms/PartnershipForm.vue';

const { t } = useI18n();

const benefits = [
  { key: 'reach', icon: 'public' },
  { key: 'support', icon: 'support_agent' },
  { key: 'growth', icon: 'trending_up' },
  { key: 'process', icon: 'verified' },
] as const;

function onDone() {}
</script>

<style scoped lang="scss">
.gc-partnership-page {
  background: var(--gc-bg);
  padding: 48px 16px 96px;

  @media (min-width: 720px) {
    padding: 80px 16px 128px;
  }
}

.gc-partnership-shell {
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 48px;
}

.gc-partnership-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
}

.gc-partnership-title {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 48px;
  }
}

.gc-partnership-subtitle {
  font-size: 15px;
  color: var(--gc-text-muted);
  margin: 0;
  max-width: 600px;
  line-height: 1.5;
}

.gc-partnership-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 32px;

  @media (min-width: 900px) {
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    align-items: start;
  }
}

.gc-partnership-info {
  background: var(--gc-bg-soft);
  border-radius: var(--gc-radius-lg);
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;

  @media (min-width: 720px) {
    padding: 40px 32px;
  }
}

.gc-info-heading {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-benefits-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.gc-benefit-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.gc-benefit-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: var(--gc-primary-soft);
  color: var(--gc-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.gc-benefit-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.gc-benefit-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--gc-text);
  letter-spacing: -0.01em;
}

.gc-benefit-desc {
  font-size: 13px;
  color: var(--gc-text-muted);
  line-height: 1.5;
}

.gc-partnership-form-wrap {
  background: var(--gc-bg);
  border: 1px solid var(--gc-border);
  border-radius: var(--gc-radius-lg);
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;

  @media (min-width: 720px) {
    padding: 40px 32px;
  }
}

.gc-form-card-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.gc-form-card-title {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-form-card-subtitle {
  font-size: 13px;
  color: var(--gc-text-muted);
  margin: 0;
}
</style>
