<template>
  <q-page class="gc-about-page">
    <section class="gc-about-hero">
      <div class="gc-about-hero-inner">
        <h1 class="gc-about-hero-title">
          {{ t('pages.about.title') }}
          <span class="gc-gradient-text">{{ t('pages.about.titleHighlight') }}</span>
        </h1>
        <p class="gc-about-hero-subtitle">{{ t('pages.about.subtitle') }}</p>
      </div>
    </section>

    <AboutStatsSection hide-heading />

    <section class="gc-mission-vision">
      <div class="gc-mv-inner">
        <article class="gc-mv-card">
          <div class="gc-mv-icon gc-mv-icon-mission">
            <q-icon name="rocket_launch" size="22px" />
          </div>
          <h2 class="gc-mv-title">{{ t('pages.about.missionTitle') }}</h2>
          <p class="gc-mv-text">{{ t('pages.about.mission') }}</p>
        </article>

        <article class="gc-mv-card">
          <div class="gc-mv-icon gc-mv-icon-vision">
            <q-icon name="visibility" size="22px" />
          </div>
          <h2 class="gc-mv-title">{{ t('pages.about.visionTitle') }}</h2>
          <p class="gc-mv-text">{{ t('pages.about.vision') }}</p>
        </article>
      </div>
    </section>

    <section class="gc-values">
      <div class="gc-values-inner">
        <h2 class="gc-values-heading">{{ t('pages.about.valuesTitle') }}</h2>

        <ul class="gc-values-grid">
          <li v-for="value in values" :key="value.key" class="gc-value-card">
            <div class="gc-value-icon">
              <q-icon :name="value.icon" size="22px" />
            </div>
            <h3 class="gc-value-title">
              {{ t(`pages.about.values.${value.key}.title`) }}
            </h3>
            <p class="gc-value-desc">
              {{ t(`pages.about.values.${value.key}.description`) }}
            </p>
          </li>
        </ul>
      </div>
    </section>

    <TeamSection />

    <ContactCtaSection />
  </q-page>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import AboutStatsSection from 'src/components/home/AboutStatsSection.vue';
import TeamSection from 'src/components/home/TeamSection.vue';
import ContactCtaSection from 'src/components/home/ContactCtaSection.vue';

const { t } = useI18n();

const values = [
  { key: 'trust', icon: 'verified_user' },
  { key: 'people', icon: 'group' },
  { key: 'results', icon: 'flag' },
  { key: 'global', icon: 'public' },
] as const;
</script>

<style scoped lang="scss">
.gc-about-page {
  background: var(--gc-bg);
}

.gc-about-hero {
  padding: 48px 16px 16px;

  @media (min-width: 720px) {
    padding: 80px 16px 24px;
  }
}

.gc-about-hero-inner {
  max-width: 720px;
  margin: 0 auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.gc-about-hero-title {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 48px;
  }
}

.gc-about-hero-subtitle {
  font-size: 15px;
  color: var(--gc-text-muted);
  margin: 0;
  max-width: 600px;
  line-height: 1.5;
}

.gc-mission-vision {
  padding: 48px 16px;

  @media (min-width: 720px) {
    padding: 64px 16px;
  }
}

.gc-mv-inner {
  max-width: 1600px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;

  @media (min-width: 720px) {
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }
}

.gc-mv-card {
  background: var(--gc-bg-soft);
  border-radius: var(--gc-radius-lg);
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;

  @media (min-width: 720px) {
    padding: 40px 32px;
  }
}

.gc-mv-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4px;
}

.gc-mv-icon-mission {
  background: var(--gc-primary-soft);
  color: var(--gc-primary);
}

.gc-mv-icon-vision {
  background: rgba(74, 141, 255, 0.12);
  color: #4a8dff;
}

.gc-mv-title {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-mv-text {
  font-size: 14px;
  color: var(--gc-text-muted);
  line-height: 1.6;
  margin: 0;
}

.gc-values {
  padding: 48px 16px;

  @media (min-width: 720px) {
    padding: 64px 16px;
  }
}

.gc-values-inner {
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.gc-values-heading {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.02em;
  text-align: center;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 36px;
  }
}

.gc-values-grid {
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

.gc-value-card {
  background: var(--gc-bg);
  border: 1px solid var(--gc-border);
  border-radius: var(--gc-radius-md);
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gc-value-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--gc-primary-soft);
  color: var(--gc-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.gc-value-title {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-value-desc {
  font-size: 13px;
  color: var(--gc-text-muted);
  line-height: 1.5;
  margin: 0;
}
</style>
