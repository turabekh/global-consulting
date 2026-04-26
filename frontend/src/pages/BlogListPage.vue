<template>
  <q-page class="gc-blog-list-page">
    <section class="gc-blog-list-hero">
      <div class="gc-blog-list-hero-inner">
        <h1 class="gc-blog-list-hero-title">
          {{ t('pages.blog.title') }}
          <span class="gc-gradient-text">{{ t('pages.blog.titleHighlight') }}</span>
        </h1>
        <p class="gc-blog-list-hero-subtitle">{{ t('pages.blog.subtitle') }}</p>
      </div>
    </section>

    <section class="gc-blog-list-content">
      <div class="gc-blog-list-inner">
        <div class="gc-blog-tabs">
          <button
            v-for="opt in categoryOptions"
            :key="opt.key"
            type="button"
            class="gc-blog-tab"
            :class="{ 'gc-blog-tab-active': active === opt.value }"
            @click="active = opt.value"
          >
            {{ t(`pages.blog.categories.${opt.key}`) }}
          </button>
        </div>

        <div v-if="loading" class="gc-blog-loading">
          <q-spinner color="primary" size="32px" />
        </div>

        <p v-else-if="posts.length === 0" class="gc-blog-empty">
          {{ t('pages.blog.empty') }}
        </p>

        <ul v-else class="gc-blog-grid">
          <li v-for="post in posts" :key="post.id" class="gc-blog-card">
            <router-link :to="`/blog/${post.slug}`" class="gc-blog-link">
              <div class="gc-blog-cover">
                <img
                  v-if="post.cover_image_url"
                  :src="post.cover_image_url"
                  :alt="post.title"
                  loading="lazy"
                />
                <div v-else class="gc-blog-cover-placeholder"></div>
              </div>
              <div class="gc-blog-meta">
                <span class="gc-blog-date">{{ formatDate(post.published_at, locale) }}</span>
              </div>
              <h2 class="gc-blog-card-title">{{ post.title }}</h2>
              <p class="gc-blog-excerpt">{{ post.excerpt }}</p>
              <span class="gc-blog-readmore">
                {{ t('home.blogPreview.readMore') }}
                <q-icon name="arrow_forward" size="14px" />
              </span>
            </router-link>
          </li>
        </ul>
      </div>
    </section>

    <ContactCtaSection />
  </q-page>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import ContactCtaSection from 'src/components/home/ContactCtaSection.vue';
import { blogService, type BlogCategory, type BlogPostListItem } from 'src/services/blog';
import { formatDate } from 'src/utils/format';

const { t, locale } = useI18n();

const posts = ref<BlogPostListItem[]>([]);
const loading = ref(true);
const active = ref<BlogCategory | null>(null);

interface CategoryOption {
  key: 'all' | BlogCategory;
  value: BlogCategory | null;
}

const categoryOptions: CategoryOption[] = [
  { key: 'all', value: null },
  { key: 'tourism', value: 'tourism' },
  { key: 'work', value: 'work' },
  { key: 'study', value: 'study' },
  { key: 'visa', value: 'visa' },
];

async function load() {
  loading.value = true;
  try {
    posts.value = await blogService.list({ category: active.value ?? undefined });
  } catch {
    posts.value = [];
  } finally {
    loading.value = false;
  }
}

onMounted(load);
watch([active, locale], load);
</script>

<style scoped lang="scss">
.gc-blog-list-page {
  background: var(--gc-bg);
}

.gc-blog-list-hero {
  padding: 48px 16px 16px;

  @media (min-width: 720px) {
    padding: 80px 16px 24px;
  }
}

.gc-blog-list-hero-inner {
  max-width: 720px;
  margin: 0 auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.gc-blog-list-hero-title {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 48px;
  }
}

.gc-blog-list-hero-subtitle {
  font-size: 15px;
  color: var(--gc-text-muted);
  margin: 0;
  max-width: 600px;
  line-height: 1.5;
}

.gc-blog-list-content {
  padding: 32px 16px 64px;
}

.gc-blog-list-inner {
  max-width: 1200px;
  margin: 0 auto;
}

.gc-blog-tabs {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px;
  margin-bottom: 32px;
}

.gc-blog-tab {
  appearance: none;
  border: none;
  background: transparent;
  color: var(--gc-text);
  font-size: 14px;
  font-weight: 500;
  padding: 8px 18px;
  border-radius: var(--gc-radius-pill);
  cursor: pointer;
  transition:
    background 0.15s ease,
    color 0.15s ease;

  &:hover {
    background: var(--gc-bg-soft);
  }
}

.gc-blog-tab-active {
  background: var(--gc-primary);
  color: #ffffff;

  &:hover {
    background: var(--gc-primary);
  }
}

.gc-blog-loading {
  display: flex;
  justify-content: center;
  padding: 48px 0;
}

.gc-blog-empty {
  text-align: center;
  color: var(--gc-text-muted);
  margin: 48px 0;
}

.gc-blog-grid {
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
    grid-template-columns: repeat(3, 1fr);
  }
}

.gc-blog-card {
  display: block;
}

.gc-blog-link {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 12px;
  border-radius: var(--gc-radius-md);
  background: var(--gc-bg);
  border: 1px solid var(--gc-border);
  text-decoration: none;
  color: inherit;
  transition:
    transform 0.15s ease,
    box-shadow 0.15s ease;
  height: 100%;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--gc-shadow-md);
  }
}

.gc-blog-cover {
  width: 100%;
  aspect-ratio: 16 / 11;
  border-radius: var(--gc-radius-sm);
  overflow: hidden;
  background: var(--gc-bg-soft);

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
}

.gc-blog-cover-placeholder {
  width: 100%;
  height: 100%;
  background: var(--gc-bg-soft);
}

.gc-blog-meta {
  font-size: 11px;
  color: var(--gc-text-muted);
  letter-spacing: 0.04em;
  padding-top: 4px;
}

.gc-blog-card-title {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  line-height: 1.3;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.gc-blog-excerpt {
  font-size: 13px;
  color: var(--gc-text-muted);
  line-height: 1.45;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.gc-blog-readmore {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--gc-primary);
  font-weight: 500;
  margin-top: auto;
}
</style>
