<template>
  <div class="gc-app-list">
    <header class="gc-app-list-header">
      <div class="gc-app-list-header-text">
        <h2 class="gc-app-list-title">{{ t('dashboard.list.title') }}</h2>
        <p class="gc-app-list-subtitle">{{ t('dashboard.list.subtitle') }}</p>
      </div>

      <q-btn
        color="primary"
        unelevated
        no-caps
        icon="add"
        :label="t('dashboard.list.newCta')"
        to="/dashboard/applications/new"
        class="gc-app-list-new-btn"
      />
    </header>

    <div class="gc-app-list-filters">
      <button
        v-for="opt in filterOptions"
        :key="opt.value"
        type="button"
        class="gc-app-list-filter"
        :class="{ 'gc-app-list-filter-active': active === opt.value }"
        @click="active = opt.value"
      >
        {{ t(`dashboard.list.filters.${opt.key}`) }}
        <span v-if="counts[opt.key]" class="gc-app-list-filter-count">{{ counts[opt.key] }}</span>
      </button>
    </div>

    <div v-if="loading" class="gc-app-list-loading">
      <q-spinner color="primary" size="32px" />
    </div>

    <div v-else-if="filtered.length === 0 && items.length === 0" class="gc-app-list-empty">
      <div class="gc-app-list-empty-icon">
        <q-icon name="inbox" size="40px" />
      </div>
      <p class="gc-app-list-empty-text">{{ t('dashboard.list.empty') }}</p>
      <q-btn
        color="primary"
        unelevated
        no-caps
        :label="t('dashboard.list.emptyAction')"
        to="/dashboard/applications/new"
        class="gc-app-list-empty-cta"
      />
    </div>

    <p v-else-if="filtered.length === 0" class="gc-app-list-empty-text">
      {{ t('home.faq.empty') }}
    </p>

    <ul v-else class="gc-app-list-items">
      <li v-for="app in filtered" :key="app.reference" class="gc-app-list-item">
        <router-link :to="`/dashboard/applications/${app.reference}`" class="gc-app-list-link">
          <div class="gc-app-list-icon" :class="`gc-app-list-icon-${app.service_type}`">
            <q-icon :name="serviceIcon(app.service_type)" size="20px" />
          </div>

          <div class="gc-app-list-content">
            <div class="gc-app-list-content-row">
              <span class="gc-app-list-item-title">
                {{ app.target_label || serviceLabel(app.service_type) }}
              </span>
              <StatusBadge :status="app.status" />
            </div>

            <div class="gc-app-list-meta">
              <span class="gc-app-list-meta-item">
                <q-icon :name="serviceIcon(app.service_type)" size="13px" />
                {{ serviceLabel(app.service_type) }}
              </span>
              <span class="gc-app-list-meta-item">
                <q-icon name="schedule" size="13px" />
                {{ formatMetaDate(app) }}
              </span>
            </div>
          </div>

          <span class="gc-app-list-action">
            {{ app.status === 'draft' ? t('dashboard.list.continue') : t('dashboard.list.view') }}
            <q-icon name="arrow_forward" size="14px" />
          </span>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import {
  applicationsService,
  type ApplicationListItem,
  type ApplicationStatus,
  type ServiceType,
} from 'src/services/applications';
import { formatDate } from 'src/utils/format';
import StatusBadge from 'src/components/dashboard/StatusBadge.vue';

const { t, locale } = useI18n();
const emit = defineEmits<{ 'page-title': [string] }>();

const items = ref<ApplicationListItem[]>([]);
const loading = ref(true);

type FilterKey = 'all' | 'drafts' | 'inProgress' | 'completed';

interface FilterOption {
  key: FilterKey;
  value: FilterKey;
}

const filterOptions: FilterOption[] = [
  { key: 'all', value: 'all' },
  { key: 'drafts', value: 'drafts' },
  { key: 'inProgress', value: 'inProgress' },
  { key: 'completed', value: 'completed' },
];

const active = ref<FilterKey>('all');

const inProgressStatuses: ApplicationStatus[] = ['submitted', 'in_review', 'needs_info'];
const completedStatuses: ApplicationStatus[] = ['accepted', 'rejected', 'closed'];

function matchesFilter(app: ApplicationListItem, filter: FilterKey): boolean {
  if (filter === 'all') return true;
  if (filter === 'drafts') return app.status === 'draft';
  if (filter === 'inProgress') return inProgressStatuses.includes(app.status);
  if (filter === 'completed') return completedStatuses.includes(app.status);
  return true;
}

const filtered = computed(() => items.value.filter((app) => matchesFilter(app, active.value)));

const counts = computed<Record<FilterKey, number>>(() => ({
  all: items.value.length,
  drafts: items.value.filter((a) => a.status === 'draft').length,
  inProgress: items.value.filter((a) => inProgressStatuses.includes(a.status)).length,
  completed: items.value.filter((a) => completedStatuses.includes(a.status)).length,
}));

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

function formatMetaDate(app: ApplicationListItem): string {
  if (app.submitted_at) {
    return t('dashboard.list.submittedOn', { date: formatDate(app.submitted_at, locale.value) });
  }
  return t('dashboard.list.lastUpdated', { date: formatDate(app.updated_at, locale.value) });
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
  emit('page-title', t('dashboard.nav.applications'));
  await load();
});

watch(locale, () => {
  emit('page-title', t('dashboard.nav.applications'));
});
</script>

<style scoped lang="scss">
.gc-app-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.gc-app-list-header {
  display: flex;
  flex-direction: column;
  gap: 16px;

  @media (min-width: 600px) {
    flex-direction: row;
    align-items: flex-end;
    justify-content: space-between;
  }
}

.gc-app-list-header-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.gc-app-list-title {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 28px;
  }
}

.gc-app-list-subtitle {
  font-size: 14px;
  color: var(--gc-text-muted);
  margin: 0;
}

.gc-app-list-new-btn {
  border-radius: var(--gc-radius-pill);
  padding: 8px 20px;
  font-weight: 600;
  align-self: flex-start;

  @media (min-width: 600px) {
    align-self: auto;
  }
}

.gc-app-list-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.gc-app-list-filter {
  appearance: none;
  border: none;
  background: transparent;
  color: var(--gc-text);
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: var(--gc-radius-pill);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition:
    background 0.15s ease,
    color 0.15s ease;

  &:hover {
    background: var(--gc-bg);
  }
}

.gc-app-list-filter-active {
  background: var(--gc-primary);
  color: #ffffff;

  &:hover {
    background: var(--gc-primary);
  }
}

.gc-app-list-filter-count {
  font-size: 11px;
  padding: 1px 6px;
  border-radius: var(--gc-radius-pill);
  background: rgba(255, 255, 255, 0.18);
  font-weight: 600;
}

.gc-app-list-filter:not(.gc-app-list-filter-active) .gc-app-list-filter-count {
  background: var(--gc-bg);
  color: var(--gc-text-muted);
}

.gc-app-list-loading {
  display: flex;
  justify-content: center;
  padding: 64px 0;
}

.gc-app-list-empty {
  background: var(--gc-bg);
  border: 1px dashed var(--gc-border);
  border-radius: var(--gc-radius-lg);
  padding: 64px 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  text-align: center;
}

.gc-app-list-empty-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: var(--gc-primary-soft);
  color: var(--gc-primary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.gc-app-list-empty-text {
  color: var(--gc-text-muted);
  margin: 0;
  font-size: 14px;
}

.gc-app-list-empty-cta {
  border-radius: var(--gc-radius-pill);
  padding: 8px 24px;
  font-weight: 600;
}

.gc-app-list-items {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.gc-app-list-item {
  display: block;
}

.gc-app-list-link {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  border-radius: var(--gc-radius-md);
  background: var(--gc-bg);
  border: 1px solid var(--gc-border);
  text-decoration: none;
  color: inherit;
  transition:
    transform 0.15s ease,
    box-shadow 0.15s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: var(--gc-shadow-sm);
  }
}

.gc-app-list-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--gc-bg-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: var(--gc-primary);
}

.gc-app-list-icon-tourism {
  color: #c97900;
}
.gc-app-list-icon-study {
  color: var(--gc-primary);
}
.gc-app-list-icon-work {
  color: #4a8dff;
}
.gc-app-list-icon-visa {
  color: #d04848;
}

.gc-app-list-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.gc-app-list-content-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.gc-app-list-item-title {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: -0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.gc-app-list-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 12px;
  color: var(--gc-text-muted);
}

.gc-app-list-meta-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.gc-app-list-action {
  display: none;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--gc-primary);
  font-weight: 500;
  flex-shrink: 0;

  @media (min-width: 720px) {
    display: inline-flex;
  }
}
</style>
