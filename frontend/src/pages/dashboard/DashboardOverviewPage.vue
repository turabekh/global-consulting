<template>
  <div class="gc-dash-overview">
    <header class="gc-dash-greeting">
      <h2 class="gc-dash-greeting-title">{{ greeting }}</h2>
      <p class="gc-dash-greeting-subtitle">{{ t('dashboard.overview.subtitle') }}</p>
    </header>

    <section class="gc-dash-stats">
      <div class="gc-dash-stat">
        <span class="gc-dash-stat-label">{{ t('dashboard.overview.stats.total') }}</span>
        <span class="gc-dash-stat-value">{{ stats.total }}</span>
      </div>
      <div class="gc-dash-stat">
        <span class="gc-dash-stat-label">{{ t('dashboard.overview.stats.drafts') }}</span>
        <span class="gc-dash-stat-value">{{ stats.drafts }}</span>
      </div>
      <div class="gc-dash-stat">
        <span class="gc-dash-stat-label">{{ t('dashboard.overview.stats.inProgress') }}</span>
        <span class="gc-dash-stat-value">{{ stats.inProgress }}</span>
      </div>
      <div class="gc-dash-stat">
        <span class="gc-dash-stat-label">{{ t('dashboard.overview.stats.completed') }}</span>
        <span class="gc-dash-stat-value">{{ stats.completed }}</span>
      </div>
    </section>

    <section class="gc-dash-card">
      <header class="gc-dash-card-header">
        <h3 class="gc-dash-card-title">{{ t('dashboard.overview.quickStartTitle') }}</h3>
        <p class="gc-dash-card-subtitle">{{ t('dashboard.overview.quickStartSubtitle') }}</p>
      </header>

      <ul class="gc-quick-start-grid">
        <li v-for="service in services" :key="service.key">
          <router-link
            :to="{ path: '/dashboard/applications/new', query: { type: service.key } }"
            class="gc-quick-start-card"
          >
            <div class="gc-quick-start-icon" :class="`gc-quick-start-icon-${service.key}`">
              <q-icon :name="service.icon" size="22px" />
            </div>
            <span class="gc-quick-start-title">
              {{ t(`dashboard.overview.serviceLabels.${service.key}`) }}
            </span>
            <span class="gc-quick-start-cta">
              {{ t('dashboard.overview.startApplication') }}
              <q-icon name="arrow_forward" size="14px" />
            </span>
          </router-link>
        </li>
      </ul>
    </section>

    <section class="gc-dash-card">
      <header class="gc-dash-card-header gc-dash-card-header-row">
        <h3 class="gc-dash-card-title">{{ t('dashboard.overview.recentTitle') }}</h3>
        <router-link to="/dashboard/applications" class="gc-dash-see-all">
          {{ t('dashboard.overview.seeAll') }}
          <q-icon name="arrow_forward" size="14px" />
        </router-link>
      </header>

      <div v-if="loading" class="gc-dash-loading">
        <q-spinner color="primary" size="32px" />
      </div>

      <p v-else-if="recent.length === 0" class="gc-dash-empty">
        {{ t('dashboard.overview.recentEmpty') }}
      </p>

      <ul v-else class="gc-recent-list">
        <li v-for="app in recent" :key="app.reference" class="gc-recent-item">
          <router-link :to="`/dashboard/applications/${app.reference}`" class="gc-recent-link">
            <div class="gc-recent-icon">
              <q-icon :name="serviceIcon(app.service_type)" size="20px" />
            </div>
            <div class="gc-recent-text">
              <span class="gc-recent-title">{{
                app.target_label || serviceLabel(app.service_type)
              }}</span>
              <span class="gc-recent-meta">
                {{ serviceLabel(app.service_type) }} • {{ formatDate(app.updated_at, locale) }}
              </span>
            </div>
            <StatusBadge :status="app.status" />
          </router-link>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useAuthStore } from 'src/stores/auth';
import {
  applicationsService,
  type ApplicationListItem,
  type ServiceType,
} from 'src/services/applications';
import { computeApplicationStats, formatDate } from 'src/utils/format';
import StatusBadge from 'src/components/dashboard/StatusBadge.vue';

const { t, locale } = useI18n();
const authStore = useAuthStore();
const emit = defineEmits<{ 'page-title': [string] }>();

const items = ref<ApplicationListItem[]>([]);
const loading = ref(true);

const services = [
  { key: 'tourism' as ServiceType, icon: 'wb_sunny' },
  { key: 'study' as ServiceType, icon: 'menu_book' },
  { key: 'work' as ServiceType, icon: 'business_center' },
  { key: 'visa' as ServiceType, icon: 'description' },
];

const greeting = computed(() => {
  const name = authStore.user?.first_name?.trim();
  if (name) {
    return t('dashboard.overview.greeting', { name });
  }
  return t('dashboard.overview.greetingFallback');
});

const stats = computed(() => computeApplicationStats(items.value));

const recent = computed(() => items.value.slice(0, 4));

function serviceLabel(type: ServiceType): string {
  return t(`dashboard.overview.serviceLabels.${type}`);
}

function serviceIcon(type: ServiceType): string {
  const map: Record<ServiceType, string> = {
    tourism: 'wb_sunny',
    study: 'menu_book',
    work: 'business_center',
    visa: 'description',
  };
  return map[type];
}

async function load() {
  loading.value = true;
  try {
    items.value = await applicationsService.list();
  } catch {
    items.value = [];
  } finally {
    loading.value = false;
  }
}

onMounted(async () => {
  emit('page-title', t('dashboard.breadcrumb.home'));
  await load();
});
</script>

<style scoped lang="scss">
.gc-dash-overview {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.gc-dash-greeting-title {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0 0 4px;

  @media (min-width: 720px) {
    font-size: 28px;
  }
}

.gc-dash-greeting-subtitle {
  font-size: 14px;
  color: var(--gc-text-muted);
  margin: 0;
}

.gc-dash-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;

  @media (min-width: 600px) {
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }
}

.gc-dash-stat {
  background: var(--gc-bg);
  border-radius: var(--gc-radius-md);
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  border: 1px solid var(--gc-border);
}

.gc-dash-stat-label {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gc-text-muted);
  font-weight: 600;
}

.gc-dash-stat-value {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--gc-text);
}

.gc-dash-card {
  background: var(--gc-bg);
  border-radius: var(--gc-radius-lg);
  padding: 24px;
  border: 1px solid var(--gc-border);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.gc-dash-card-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.gc-dash-card-header-row {
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.gc-dash-card-title {
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-dash-card-subtitle {
  font-size: 13px;
  color: var(--gc-text-muted);
  margin: 0;
}

.gc-dash-see-all {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--gc-primary);
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
}

.gc-quick-start-grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;

  @media (min-width: 600px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (min-width: 1100px) {
    grid-template-columns: repeat(4, 1fr);
  }
}

.gc-quick-start-card {
  background: var(--gc-bg-soft);
  border-radius: var(--gc-radius-md);
  padding: 18px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  text-decoration: none;
  color: inherit;
  transition:
    transform 0.15s ease,
    background 0.15s ease;

  &:hover {
    transform: translateY(-2px);
    background: var(--gc-primary-soft);
  }
}

.gc-quick-start-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gc-bg);
  color: var(--gc-primary);
}

.gc-quick-start-icon-tourism {
  color: #c97900;
}
.gc-quick-start-icon-study {
  color: var(--gc-primary);
}
.gc-quick-start-icon-work {
  color: #4a8dff;
}
.gc-quick-start-icon-visa {
  color: #d04848;
}

.gc-quick-start-title {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.gc-quick-start-cta {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--gc-text-muted);
  font-weight: 500;
  margin-top: auto;
}

.gc-dash-loading {
  display: flex;
  justify-content: center;
  padding: 32px 0;
}

.gc-dash-empty {
  text-align: center;
  color: var(--gc-text-muted);
  margin: 16px 0;
}

.gc-recent-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.gc-recent-item {
  display: block;
}

.gc-recent-link {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 14px;
  border-radius: var(--gc-radius-md);
  background: var(--gc-bg-soft);
  text-decoration: none;
  color: inherit;
  transition: background 0.15s ease;

  &:hover {
    background: var(--gc-border);
  }
}

.gc-recent-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--gc-bg);
  color: var(--gc-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.gc-recent-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
  min-width: 0;
}

.gc-recent-title {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: -0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.gc-recent-meta {
  font-size: 12px;
  color: var(--gc-text-muted);
}
</style>
