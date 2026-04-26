<template>
  <q-page class="gc-testimonials-page">
    <section class="gc-testimonials-hero">
      <div class="gc-testimonials-hero-inner">
        <h1 class="gc-testimonials-hero-title">
          {{ t('pages.testimonials.title') }}
          <span class="gc-gradient-text">{{ t('pages.testimonials.titleHighlight') }}</span>
        </h1>
        <p class="gc-testimonials-hero-subtitle">{{ t('pages.testimonials.subtitle') }}</p>
      </div>
    </section>

    <TestimonialsSection grid-only />

    <ContactCtaSection />
  </q-page>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import TestimonialsSection from 'src/components/home/TestimonialsSection.vue';
import ContactCtaSection from 'src/components/home/ContactCtaSection.vue';

const { t } = useI18n();
</script>

<style scoped lang="scss">
.gc-testimonials-page {
  background: var(--gc-bg);
}

.gc-testimonials-hero {
  padding: 48px 16px 16px;

  @media (min-width: 720px) {
    padding: 80px 16px 24px;
  }
}

.gc-testimonials-hero-inner {
  max-width: 720px;
  margin: 0 auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.gc-testimonials-hero-title {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 48px;
  }
}

.gc-testimonials-hero-subtitle {
  font-size: 15px;
  color: var(--gc-text-muted);
  margin: 0;
  max-width: 600px;
  line-height: 1.5;
}
</style>
