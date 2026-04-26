<template>
  <section class="gc-testimonials">
    <div class="gc-testimonials-inner">
      <aside class="gc-testimonials-side">
        <h2 class="gc-testimonials-title">
          {{ t('home.testimonials.titlePart1') }}
          <span class="gc-gradient-text">{{ t('home.testimonials.titleHighlight1') }}</span>
          <br />
          {{ t('home.testimonials.titlePart2') }}
          <span class="gc-gradient-text">{{ t('home.testimonials.titleHighlight2') }}</span>
        </h2>
        <p class="gc-testimonials-subtitle">
          {{ t('home.testimonials.subtitle') }}
          <span class="gc-testimonials-emoji" aria-hidden="true">👉</span>
        </p>
        <q-btn
          color="primary"
          unelevated
          no-caps
          :label="t('home.testimonials.cta')"
          to="/signup"
          class="gc-testimonials-cta"
        />
      </aside>

      <div class="gc-testimonials-content">
        <div v-if="loading" class="gc-testimonials-loading">
          <q-spinner color="primary" size="32px" />
        </div>

        <p v-else-if="items.length === 0" class="gc-testimonials-empty">
          {{ t('home.testimonials.empty') }}
        </p>

        <div v-else class="gc-testimonials-masonry">
          <article v-for="item in items" :key="item.id" class="gc-testimonial-card">
            <div class="gc-testimonial-body" v-html="item.body_html"></div>
            <footer class="gc-testimonial-author">
              <q-avatar size="36px" class="gc-testimonial-avatar">
                <img
                  v-if="item.author_photo_url"
                  :src="item.author_photo_url"
                  :alt="item.author_name"
                />
                <span v-else class="gc-testimonial-initials">{{
                  initialsFor(item.author_name)
                }}</span>
              </q-avatar>
              <div class="gc-testimonial-author-text">
                <span class="gc-testimonial-author-name">{{ item.author_name }}</span>
                <span v-if="item.author_city" class="gc-testimonial-author-city">{{
                  item.author_city
                }}</span>
              </div>
            </footer>
          </article>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { testimonialsService, type Testimonial } from 'src/services/testimonials';

const { t, locale } = useI18n();

const items = ref<Testimonial[]>([]);
const loading = ref(true);

async function load() {
  loading.value = true;
  try {
    items.value = await testimonialsService.list();
  } catch {
    items.value = [];
  } finally {
    loading.value = false;
  }
}

function initialsFor(name: string): string {
  return name
    .split(' ')
    .map((part) => part[0]?.toUpperCase() ?? '')
    .filter(Boolean)
    .slice(0, 2)
    .join('');
}

onMounted(load);
watch(locale, load);
</script>

<style scoped lang="scss">
.gc-testimonials {
  padding: 48px 16px;

  @media (min-width: 720px) {
    padding: 80px 16px;
  }
}

.gc-testimonials-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr;
  gap: 32px;

  @media (min-width: 900px) {
    grid-template-columns: 1fr 2fr;
    gap: 48px;
  }
}

.gc-testimonials-side {
  display: flex;
  flex-direction: column;
  gap: 20px;

  @media (min-width: 900px) {
    padding-top: 24px;
    align-self: flex-start;
    position: sticky;
    top: 96px;
  }
}

.gc-testimonials-title {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 40px;
  }
}

.gc-testimonials-subtitle {
  font-size: 14px;
  color: var(--gc-text-muted);
  margin: 0;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.gc-testimonials-emoji {
  font-size: 16px;
}

.gc-testimonials-cta {
  border-radius: var(--gc-radius-pill);
  font-weight: 600;
  padding: 8px 24px;
  align-self: flex-start;
}

.gc-testimonials-loading {
  display: flex;
  justify-content: center;
  padding: 48px 0;
}

.gc-testimonials-empty {
  text-align: center;
  color: var(--gc-text-muted);
  margin: 48px 0;
}

.gc-testimonials-masonry {
  columns: 1;
  column-gap: 16px;

  @media (min-width: 600px) {
    columns: 2;
    column-gap: 16px;
  }
}

.gc-testimonial-card {
  break-inside: avoid;
  margin: 0 0 16px;
  background: var(--gc-bg-soft);
  border-radius: var(--gc-radius-md);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.gc-testimonial-body {
  font-size: 14px;
  color: var(--gc-text);
  line-height: 1.55;

  :deep(p) {
    margin: 0 0 12px;
  }

  :deep(p:last-child) {
    margin-bottom: 0;
  }

  :deep(strong) {
    font-weight: 700;
    color: var(--gc-text);
  }

  :deep(em) {
    font-style: italic;
  }

  :deep(a) {
    color: var(--gc-primary);
    text-decoration: underline;
  }
}

.gc-testimonial-author {
  display: flex;
  align-items: center;
  gap: 10px;
}

.gc-testimonial-avatar {
  flex-shrink: 0;
}

.gc-testimonial-initials {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gc-primary-soft);
  color: var(--gc-primary);
  font-weight: 600;
  font-size: 12px;
}

.gc-testimonial-author-text {
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 0;
}

.gc-testimonial-author-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--gc-text);
}

.gc-testimonial-author-city {
  font-size: 12px;
  color: var(--gc-text-muted);
}
</style>
