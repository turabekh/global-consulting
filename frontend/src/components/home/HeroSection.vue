<template>
  <section class="gc-hero">
    <div class="gc-hero-inner">
      <div class="gc-hero-emoji-cap" aria-hidden="true">🎓</div>

      <span class="gc-hero-emoji gc-hero-emoji-plane" aria-hidden="true">✈️</span>
      <span class="gc-hero-emoji gc-hero-emoji-briefcase" aria-hidden="true">💼</span>

      <h1 class="gc-hero-title">
        {{ t('home.hero.titlePart1') }}
        <span class="gc-gradient-text">{{ t('home.hero.titleHighlight1') }}</span>
        {{ t('home.hero.titlePart2') }}
        <span class="gc-gradient-text">{{ t('home.hero.titleHighlight2') }}</span>
      </h1>

      <p class="gc-hero-subtitle">{{ t('home.hero.subtitle') }}</p>

      <q-btn
        unelevated
        no-caps
        size="lg"
        class="gc-hero-cta"
        :label="t('home.hero.cta')"
        to="/services"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>

<style scoped lang="scss">
.gc-hero {
  position: relative;
  padding: 64px 16px 32px;
  overflow: hidden;
}

.gc-hero-inner {
  position: relative;
  max-width: 880px;
  margin: 0 auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.gc-hero-emoji-cap {
  font-size: 56px;
  line-height: 1;
  margin-bottom: 8px;
}

.gc-hero-emoji {
  position: absolute;
  font-size: 40px;
  line-height: 1;
  user-select: none;
  pointer-events: none;
  display: none;

  @media (min-width: 720px) {
    display: block;
  }
}

.gc-hero-emoji-plane {
  top: 38%;
  left: 4%;
  transform: rotate(-12deg);
}

.gc-hero-emoji-briefcase {
  top: 38%;
  right: 4%;
  transform: rotate(8deg);
}

.gc-hero-title {
  font-size: 40px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 56px;
  }

  @media (min-width: 1024px) {
    font-size: 64px;
  }
}

.gc-hero-subtitle {
  font-size: 16px;
  color: var(--gc-text-muted);
  margin: 0;
  max-width: 520px;
}

.gc-hero-cta {
  border-radius: var(--gc-radius-pill);
  font-weight: 600;
  padding: 12px 28px;
  background: linear-gradient(90deg, #4a8dff 0%, #ff5577 50%, #ff6b6b 100%);
  color: #ffffff;
  border: none;
  box-shadow: 0 8px 24px rgba(255, 85, 119, 0.25);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 28px rgba(255, 85, 119, 0.32);
  }

  :deep(.q-btn__content) {
    font-size: 15px;
    letter-spacing: 0.01em;
  }
}
</style>
