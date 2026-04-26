<template>
  <section class="gc-contact-cta">
    <div class="gc-contact-cta-inner">
      <h2 class="gc-contact-cta-title">
        <span class="gc-gradient-text">{{ t('home.contactCta.titlePart1') }}</span>
        <span class="gc-gradient-text">{{ t('home.contactCta.titleHighlight') }}</span>
        {{ t('home.contactCta.titlePart2') }}
      </h2>

      <q-btn
        color="primary"
        unelevated
        no-caps
        size="lg"
        :label="t('home.contactCta.cta')"
        to="/contact"
        class="gc-contact-cta-btn"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>

<style scoped lang="scss">
.gc-contact-cta {
  padding: 64px 16px 32px;
}

.gc-contact-cta-inner {
  max-width: 720px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 32px;
}

.gc-contact-cta-title {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.2;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 36px;
  }
}

.gc-contact-cta-btn {
  border-radius: var(--gc-radius-pill);
  font-weight: 600;
  padding: 12px 32px;
}
</style>
