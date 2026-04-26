<template>
  <q-page v-if="serviceConfig" class="gc-service-detail">
    <section class="gc-service-hero" :class="`gc-service-hero-${serviceType}`">
      <div class="gc-service-hero-inner">
        <div class="gc-service-hero-icon">
          <q-icon :name="serviceConfig.icon" size="32px" />
        </div>
        <h1 class="gc-service-hero-title">
          <span class="gc-gradient-text">
            {{ t(`pages.serviceDetail.${serviceType}.title`) }}
          </span>
        </h1>
        <p class="gc-service-hero-subtitle">
          {{ t(`pages.serviceDetail.${serviceType}.subtitle`) }}
        </p>

        <div class="gc-service-hero-ctas">
          <q-btn
            color="primary"
            unelevated
            no-caps
            size="md"
            :label="t('home.contactCta.cta')"
            class="gc-hero-cta-primary"
            @click="dialogs.openContact()"
          />
          <q-btn
            outline
            no-caps
            size="md"
            :label="t('home.blogPreview.seeOther')"
            class="gc-hero-cta-secondary"
            to="/blog"
          />
        </div>
      </div>
    </section>

    <section class="gc-service-features">
      <div class="gc-service-features-inner">
        <h2 class="gc-section-heading">
          {{ t('pages.serviceDetail.featuresHeading') }}
        </h2>

        <ul class="gc-features-grid">
          <li v-for="key in serviceConfig.featureKeys" :key="key" class="gc-feature-card">
            <div class="gc-feature-icon">
              <q-icon :name="featureIcons[key]" size="22px" />
            </div>
            <h3 class="gc-feature-title">
              {{ t(`pages.serviceDetail.${serviceType}.features.${key}.title`) }}
            </h3>
            <p class="gc-feature-desc">
              {{ t(`pages.serviceDetail.${serviceType}.features.${key}.description`) }}
            </p>
          </li>
        </ul>
      </div>
    </section>

    <section class="gc-service-catalog">
      <div class="gc-service-catalog-inner">
        <h2 class="gc-section-heading">
          {{ t(`pages.serviceDetail.${serviceType}.catalogTitle`) }}
        </h2>

        <div v-if="loading" class="gc-catalog-loading">
          <q-spinner color="primary" size="32px" />
        </div>

        <p v-else-if="items.length === 0" class="gc-catalog-empty">
          {{ t(`pages.serviceDetail.${serviceType}.catalogEmpty`) }}
        </p>

        <ul v-else class="gc-catalog-grid">
          <li v-for="item in items" :key="item.id" class="gc-catalog-card">
            <div class="gc-catalog-cover">
              <img
                v-if="item.cover_image_url"
                :src="item.cover_image_url"
                :alt="item.title"
                loading="lazy"
              />
              <div v-else class="gc-catalog-cover-placeholder"></div>
            </div>
            <div class="gc-catalog-content">
              <h3 class="gc-catalog-title">{{ item.title }}</h3>
              <p class="gc-catalog-meta">{{ describeItem(item) }}</p>
              <p class="gc-catalog-desc">{{ item.description }}</p>
              <p class="gc-catalog-stat">{{ statForItem(item) }}</p>
            </div>
          </li>
        </ul>
      </div>
    </section>

    <FaqSection />

    <section v-if="!relatedLoading && relatedPosts.length > 0" class="gc-service-related">
      <div class="gc-service-related-inner">
        <h2 class="gc-section-heading">
          {{ t('pages.serviceDetail.relatedBlogTitle') }}
        </h2>
        <ul class="gc-related-grid">
          <li v-for="post in relatedPosts" :key="post.id" class="gc-related-card">
            <router-link :to="`/blog/${post.slug}`" class="gc-related-link">
              <div class="gc-related-cover">
                <img
                  v-if="post.cover_image_url"
                  :src="post.cover_image_url"
                  :alt="post.title"
                  loading="lazy"
                />
                <div v-else class="gc-related-cover-placeholder"></div>
              </div>
              <span class="gc-related-date">
                {{ formatDate(post.published_at, locale) }}
              </span>
              <h3 class="gc-related-title">{{ post.title }}</h3>
              <p class="gc-related-excerpt">{{ post.excerpt }}</p>
            </router-link>
          </li>
        </ul>
      </div>
    </section>

    <ContactCtaSection />
  </q-page>

  <q-page v-else class="gc-service-detail">
    <div class="gc-service-not-found">
      <h1>404</h1>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';
import FaqSection from 'src/components/home/FaqSection.vue';
import ContactCtaSection from 'src/components/home/ContactCtaSection.vue';
import { useDialogsStore } from 'src/stores/dialogs';
import { formatDate } from 'src/utils/format';
import {
  tourPackagesService,
  universitiesService,
  jobsService,
  visaTypesService,
  type TourPackage,
  type University,
  type Job,
  type VisaType,
} from 'src/services/catalog';
import { blogService, type BlogPostListItem, type BlogCategory } from 'src/services/blog';

type ServiceType = 'tourism' | 'study' | 'work' | 'visa';
type CatalogItem = TourPackage | University | Job | VisaType;

interface ServiceConfig {
  icon: string;
  blogCategory: BlogCategory;
  featureKeys: readonly string[];
  loadItems: () => Promise<CatalogItem[]>;
}

const { t, locale } = useI18n();
const route = useRoute();
const dialogs = useDialogsStore();

const items = ref<CatalogItem[]>([]);
const loading = ref(true);
const relatedPosts = ref<BlogPostListItem[]>([]);
const relatedLoading = ref(true);

const featureIcons: Record<string, string> = {
  curated: 'tune',
  local: 'location_on',
  flexible: 'event',
  support: 'support_agent',
  match: 'school',
  application: 'description',
  scholarships: 'savings',
  settle: 'home',
  vetted: 'verified',
  coaching: 'record_voice_over',
  relocation: 'flight_takeoff',
  ongoing: 'autorenew',
  assessment: 'fact_check',
  documents: 'task',
  tracking: 'pending_actions',
  interview: 'forum',
};

const SERVICE_CONFIG: Record<ServiceType, ServiceConfig> = {
  tourism: {
    icon: 'wb_sunny',
    blogCategory: 'tourism',
    featureKeys: ['curated', 'local', 'flexible', 'support'],
    loadItems: () => tourPackagesService.list(),
  },
  study: {
    icon: 'menu_book',
    blogCategory: 'study',
    featureKeys: ['match', 'application', 'scholarships', 'settle'],
    loadItems: () => universitiesService.list(),
  },
  work: {
    icon: 'business_center',
    blogCategory: 'work',
    featureKeys: ['vetted', 'coaching', 'relocation', 'ongoing'],
    loadItems: () => jobsService.list(),
  },
  visa: {
    icon: 'description',
    blogCategory: 'visa',
    featureKeys: ['assessment', 'documents', 'tracking', 'interview'],
    loadItems: () => visaTypesService.list(),
  },
};

const serviceType = computed<ServiceType | null>(() => {
  const param = route.params.type as string | undefined;
  if (!param) return null;
  if (param in SERVICE_CONFIG) return param as ServiceType;
  return null;
});

const serviceConfig = computed(() =>
  serviceType.value ? SERVICE_CONFIG[serviceType.value] : null,
);

function isTourPackage(item: CatalogItem): item is TourPackage {
  return 'duration_days' in item;
}
function isUniversity(item: CatalogItem): item is University {
  return 'tuition_from' in item;
}
function isJob(item: CatalogItem): item is Job {
  return 'employment_type' in item;
}
function isVisaType(item: CatalogItem): item is VisaType {
  return 'processing_time' in item && !('duration_days' in item);
}

function describeItem(item: CatalogItem): string {
  if (isTourPackage(item)) {
    return item.destination;
  }
  if (isUniversity(item)) {
    return item.city ? `${item.city}, ${item.country}` : item.country;
  }
  if (isJob(item)) {
    const place = item.city ? `${item.city}, ${item.country}` : item.country;
    return item.industry ? `${place} • ${item.industry}` : place;
  }
  if (isVisaType(item)) {
    return item.country;
  }
  return '';
}

function statForItem(item: CatalogItem): string {
  if (!serviceType.value) return '';

  if (isTourPackage(item)) {
    const parts: string[] = [];
    if (item.duration_days > 0) {
      parts.push(`${item.duration_days} ${t('pages.serviceDetail.tourism.durationLabel')}`);
    }
    if (item.price_from) {
      parts.push(
        `${t('pages.serviceDetail.tourism.priceFrom')} ${item.price_from} ${item.currency}`,
      );
    }
    return parts.join(' • ');
  }

  if (isUniversity(item)) {
    const parts: string[] = [];
    if (item.world_ranking) {
      parts.push(`#${item.world_ranking} ${t('pages.serviceDetail.study.rankingLabel')}`);
    }
    if (item.tuition_from) {
      parts.push(
        `${t('pages.serviceDetail.study.tuitionFrom')} ${item.tuition_from} ${item.currency}`,
      );
    }
    return parts.join(' • ');
  }

  if (isJob(item)) {
    const parts: string[] = [];
    parts.push(t(`pages.serviceDetail.work.employmentTypes.${item.employment_type}`));
    if (item.salary_from) {
      const range = item.salary_to
        ? `${item.salary_from} – ${item.salary_to}`
        : `${item.salary_from}+`;
      parts.push(`${t('pages.serviceDetail.work.salaryRange')} ${range} ${item.currency}`);
    }
    return parts.join(' • ');
  }

  if (isVisaType(item)) {
    const parts: string[] = [];
    parts.push(t(`pages.serviceDetail.visa.categories.${item.category}`));
    if (item.processing_time) {
      parts.push(`${t('pages.serviceDetail.visa.processingLabel')}: ${item.processing_time}`);
    }
    if (item.success_rate !== null) {
      parts.push(`${t('pages.serviceDetail.visa.successRateLabel')}: ${item.success_rate}%`);
    }
    return parts.join(' • ');
  }

  return '';
}

async function loadItems() {
  if (!serviceConfig.value) return;
  loading.value = true;
  try {
    items.value = await serviceConfig.value.loadItems();
  } catch {
    items.value = [];
  } finally {
    loading.value = false;
  }
}

async function loadRelated() {
  if (!serviceConfig.value) return;
  relatedLoading.value = true;
  try {
    const posts = await blogService.list({ category: serviceConfig.value.blogCategory });
    relatedPosts.value = posts.slice(0, 3);
  } catch {
    relatedPosts.value = [];
  } finally {
    relatedLoading.value = false;
  }
}

async function loadAll() {
  await Promise.all([loadItems(), loadRelated()]);
}

onMounted(loadAll);
watch([() => route.params.type, locale], loadAll);
</script>

<style scoped lang="scss">
.gc-service-detail {
  background: var(--gc-bg);
}

.gc-service-hero {
  padding: 64px 16px 48px;

  @media (min-width: 720px) {
    padding: 96px 16px 64px;
  }
}

.gc-service-hero-tourism {
  background: linear-gradient(180deg, rgba(255, 196, 86, 0.08) 0%, transparent 100%);
}
.gc-service-hero-study {
  background: linear-gradient(180deg, rgba(110, 94, 246, 0.08) 0%, transparent 100%);
}
.gc-service-hero-work {
  background: linear-gradient(180deg, rgba(74, 141, 255, 0.08) 0%, transparent 100%);
}
.gc-service-hero-visa {
  background: linear-gradient(180deg, rgba(255, 107, 107, 0.08) 0%, transparent 100%);
}

.gc-service-hero-inner {
  max-width: 720px;
  margin: 0 auto;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.gc-service-hero-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: var(--gc-primary-soft);
  color: var(--gc-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.gc-service-hero-title {
  font-size: 36px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.05;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 56px;
  }
}

.gc-service-hero-subtitle {
  font-size: 16px;
  color: var(--gc-text-muted);
  margin: 0;
  max-width: 600px;
  line-height: 1.5;
}

.gc-service-hero-ctas {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin-top: 8px;
}

.gc-hero-cta-primary,
.gc-hero-cta-secondary {
  border-radius: var(--gc-radius-pill);
  font-weight: 600;
  padding: 8px 24px;
}

.gc-hero-cta-secondary {
  color: var(--gc-text);
  border-color: var(--gc-border);
}

.gc-section-heading {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.02em;
  text-align: center;
  margin: 0 0 32px;

  @media (min-width: 720px) {
    font-size: 36px;
  }
}

.gc-service-features {
  padding: 48px 16px;

  @media (min-width: 720px) {
    padding: 64px 16px;
  }
}

.gc-service-features-inner {
  max-width: 1200px;
  margin: 0 auto;
}

.gc-features-grid {
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

.gc-feature-card {
  background: var(--gc-bg);
  border: 1px solid var(--gc-border);
  border-radius: var(--gc-radius-md);
  padding: 24px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gc-feature-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--gc-primary-soft);
  color: var(--gc-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.gc-feature-title {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-feature-desc {
  font-size: 13px;
  color: var(--gc-text-muted);
  line-height: 1.5;
  margin: 0;
}

.gc-service-catalog {
  padding: 48px 16px;
  background: var(--gc-bg-soft);

  @media (min-width: 720px) {
    padding: 64px 16px;
  }
}

.gc-service-catalog-inner {
  max-width: 1200px;
  margin: 0 auto;
}

.gc-catalog-loading {
  display: flex;
  justify-content: center;
  padding: 48px 0;
}

.gc-catalog-empty {
  text-align: center;
  color: var(--gc-text-muted);
  margin: 48px 0;
}

.gc-catalog-grid {
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

.gc-catalog-card {
  background: var(--gc-bg);
  border-radius: var(--gc-radius-md);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.gc-catalog-cover {
  width: 100%;
  aspect-ratio: 16 / 11;
  background: var(--gc-bg-soft);

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
}

.gc-catalog-cover-placeholder {
  width: 100%;
  height: 100%;
  background: var(--gc-bg-soft);
}

.gc-catalog-content {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.gc-catalog-title {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-catalog-meta {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--gc-primary);
  font-weight: 500;
  margin: 0;
}

.gc-catalog-desc {
  font-size: 13px;
  color: var(--gc-text-muted);
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.gc-catalog-stat {
  font-size: 13px;
  color: var(--gc-text);
  font-weight: 500;
  margin: 4px 0 0;
}

.gc-service-related {
  padding: 48px 16px;

  @media (min-width: 720px) {
    padding: 64px 16px;
  }
}

.gc-service-related-inner {
  max-width: 1200px;
  margin: 0 auto;
}

.gc-related-grid {
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

.gc-related-card {
  display: block;
}

.gc-related-link {
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

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--gc-shadow-md);
  }
}

.gc-related-cover {
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

.gc-related-cover-placeholder {
  width: 100%;
  height: 100%;
  background: var(--gc-bg-soft);
}

.gc-related-date {
  font-size: 11px;
  color: var(--gc-text-muted);
  letter-spacing: 0.04em;
}

.gc-related-title {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: -0.01em;
  line-height: 1.3;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.gc-related-excerpt {
  font-size: 13px;
  color: var(--gc-text-muted);
  line-height: 1.45;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.gc-service-not-found {
  padding: 96px 16px;
  text-align: center;
}
</style>
