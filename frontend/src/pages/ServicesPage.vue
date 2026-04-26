<template>
  <q-page class="gc-services-page">
    <section class="gc-services-hero">
      <div class="gc-services-hero-inner">
        <h1 class="gc-services-hero-title">
          {{ t('pages.services.title') }}
          <span class="gc-gradient-text">{{ t('pages.services.titleHighlight') }}</span>
        </h1>
        <p class="gc-services-hero-subtitle">{{ t('pages.services.subtitle') }}</p>
      </div>
    </section>

    <ServicesPreviewSection />

    <FaqSection />

    <ContactCtaSection />
  </q-page>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import ServicesPreviewSection from 'src/components/home/ServicesPreviewSection.vue';
import FaqSection from 'src/components/home/FaqSection.vue';
import ContactCtaSection from 'src/components/home/ContactCtaSection.vue';

const { t } = useI18n();
</script>

<style scoped lang="scss">
.gc-services-page {
  background: var(--gc-bg);
}

.gc-services-hero {
  padding: 48px 16px 16px;

  @media (min-width: 720px) {
    padding: 80px 16px 24px;
  }
}

.gc-services-hero-inner {
  max-width: 720px;
  margin: 0 auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.gc-services-hero-title {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 48px;
  }
}

.gc-services-hero-subtitle {
  font-size: 15px;
  color: var(--gc-text-muted);
  margin: 0;
  max-width: 600px;
  line-height: 1.5;
}
</style>
