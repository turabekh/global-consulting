<template>
  <q-page class="gc-blog-detail-page">
    <div v-if="loading" class="gc-blog-detail-loading">
      <q-spinner color="primary" size="32px" />
    </div>

    <div v-else-if="!post" class="gc-blog-not-found">
      <h1 class="gc-not-found-title">{{ t('pages.blogDetail.notFound') }}</h1>
      <p class="gc-not-found-text">{{ t('pages.blogDetail.notFoundMessage') }}</p>
      <q-btn
        outline
        no-caps
        :label="t('pages.blogDetail.backToBlog')"
        to="/blog"
        class="gc-back-btn"
      />
    </div>

    <article v-else class="gc-blog-article">
      <div class="gc-blog-article-inner">
        <router-link to="/blog" class="gc-back-link">
          <q-icon name="arrow_back" size="14px" />
          {{ t('pages.blogDetail.backToBlog') }}
        </router-link>

        <header class="gc-article-header">
          <div class="gc-article-meta">
            <span class="gc-article-category">
              {{ t(`pages.blogDetail.categoryLabels.${post.category}`) }}
            </span>
            <span class="gc-article-meta-divider">•</span>
            <span class="gc-article-date">
              {{ formatDate(post.published_at, locale) }}
            </span>
            <span class="gc-article-meta-divider">•</span>
            <span class="gc-article-read-time">
              {{ post.read_time_minutes }} {{ t('pages.blogDetail.readTime') }}
            </span>
          </div>

          <h1 class="gc-article-title">{{ post.title }}</h1>
          <p v-if="post.excerpt" class="gc-article-excerpt">{{ post.excerpt }}</p>
        </header>

        <div v-if="post.cover_image_url" class="gc-article-cover">
          <img :src="post.cover_image_url" :alt="post.title" />
        </div>

        <div class="gc-article-layout">
          <div class="gc-article-body" v-html="post.body_html"></div>

          <aside v-if="recommended.length > 0" class="gc-article-aside">
            <h2 class="gc-aside-title">{{ t('pages.blogDetail.recommendedTitle') }}</h2>
            <ul class="gc-aside-list">
              <li v-for="rec in recommended" :key="rec.id" class="gc-aside-item">
                <router-link :to="`/blog/${rec.slug}`" class="gc-aside-link">
                  <div class="gc-aside-cover">
                    <img
                      v-if="rec.cover_image_url"
                      :src="rec.cover_image_url"
                      :alt="rec.title"
                      loading="lazy"
                    />
                    <div v-else class="gc-aside-cover-placeholder"></div>
                  </div>
                  <div class="gc-aside-text">
                    <span class="gc-aside-date">{{ formatDate(rec.published_at, locale) }}</span>
                    <h3 class="gc-aside-card-title">{{ rec.title }}</h3>
                  </div>
                </router-link>
              </li>
            </ul>
          </aside>
        </div>
      </div>
    </article>

    <ContactCtaSection />
  </q-page>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';
import ContactCtaSection from 'src/components/home/ContactCtaSection.vue';
import { blogService, type BlogPostDetail, type BlogPostListItem } from 'src/services/blog';
import { formatDate } from 'src/utils/format';

const { t, locale } = useI18n();
const route = useRoute();

const post = ref<BlogPostDetail | null>(null);
const recommended = ref<BlogPostListItem[]>([]);
const loading = ref(true);

async function loadPost() {
  const slug = route.params.slug as string;
  if (!slug) {
    post.value = null;
    return;
  }
  try {
    post.value = await blogService.detail(slug);
  } catch {
    post.value = null;
  }
}

async function loadRecommended() {
  if (!post.value) {
    recommended.value = [];
    return;
  }
  try {
    const all = await blogService.list({ category: post.value.category });
    recommended.value = all.filter((p) => p.slug !== post.value?.slug).slice(0, 3);
  } catch {
    recommended.value = [];
  }
}

async function loadAll() {
  loading.value = true;
  try {
    await loadPost();
    await loadRecommended();
  } finally {
    loading.value = false;
  }
}

onMounted(loadAll);
watch([() => route.params.slug, locale], loadAll);
</script>

<style scoped lang="scss">
.gc-blog-detail-page {
  background: var(--gc-bg);
}

.gc-blog-detail-loading {
  display: flex;
  justify-content: center;
  padding: 96px 16px;
}

.gc-blog-not-found {
  padding: 96px 16px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.gc-not-found-title {
  font-size: 28px;
  font-weight: 700;
  margin: 0;
}

.gc-not-found-text {
  color: var(--gc-text-muted);
  margin: 0;
}

.gc-back-btn {
  border-radius: var(--gc-radius-pill);
  padding: 6px 24px;
}

.gc-blog-article {
  padding: 32px 16px 64px;

  @media (min-width: 720px) {
    padding: 48px 16px 80px;
  }
}

.gc-blog-article-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.gc-back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--gc-text-muted);
  text-decoration: none;
  font-weight: 500;
  align-self: flex-start;

  &:hover {
    color: var(--gc-primary);
  }
}

.gc-article-header {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 720px;
}

.gc-article-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: var(--gc-text-muted);
  letter-spacing: 0.02em;
}

.gc-article-category {
  background: var(--gc-primary-soft);
  color: var(--gc-primary);
  padding: 4px 10px;
  border-radius: var(--gc-radius-pill);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  font-size: 11px;
}

.gc-article-meta-divider {
  color: var(--gc-border);
}

.gc-article-title {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.15;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 44px;
  }
}

.gc-article-excerpt {
  font-size: 17px;
  color: var(--gc-text-muted);
  line-height: 1.5;
  margin: 0;
}

.gc-article-cover {
  width: 100%;
  border-radius: var(--gc-radius-lg);
  overflow: hidden;
  background: var(--gc-bg-soft);

  img {
    width: 100%;
    height: auto;
    display: block;
    aspect-ratio: 16 / 9;
    object-fit: cover;
  }
}

.gc-article-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 32px;

  @media (min-width: 1000px) {
    grid-template-columns: minmax(0, 720px) 1fr;
    gap: 56px;
  }
}

.gc-article-body {
  font-size: 16px;
  line-height: 1.7;
  color: var(--gc-text);

  :deep(p) {
    margin: 0 0 18px;
  }

  :deep(p:last-child) {
    margin-bottom: 0;
  }

  :deep(strong) {
    font-weight: 600;
  }

  :deep(em) {
    font-style: italic;
  }

  :deep(a) {
    color: var(--gc-primary);
    text-decoration: underline;
  }

  :deep(ul),
  :deep(ol) {
    margin: 0 0 18px;
    padding-left: 24px;
  }

  :deep(li) {
    margin-bottom: 6px;
  }

  :deep(li:last-child) {
    margin-bottom: 0;
  }
}

.gc-article-aside {
  align-self: flex-start;

  @media (min-width: 1000px) {
    position: sticky;
    top: 96px;
  }
}

.gc-aside-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0 0 16px;
}

.gc-aside-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gc-aside-link {
  display: flex;
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

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--gc-shadow-sm);
  }
}

.gc-aside-cover {
  width: 96px;
  aspect-ratio: 1 / 1;
  border-radius: var(--gc-radius-sm);
  overflow: hidden;
  background: var(--gc-bg-soft);
  flex-shrink: 0;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
}

.gc-aside-cover-placeholder {
  width: 100%;
  height: 100%;
  background: var(--gc-bg-soft);
}

.gc-aside-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.gc-aside-date {
  font-size: 11px;
  color: var(--gc-text-muted);
  letter-spacing: 0.04em;
}

.gc-aside-card-title {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: -0.01em;
  line-height: 1.35;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
