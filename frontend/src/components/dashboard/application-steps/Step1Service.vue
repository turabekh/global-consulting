<template>
  <div class="gc-step1">
    <header class="gc-step-section-header">
      <h3 class="gc-step-section-title">{{ t('dashboard.edit.serviceStep.heading') }}</h3>
      <p class="gc-step-section-sub">{{ t('dashboard.edit.serviceStep.subheading') }}</p>
    </header>

    <ul class="gc-service-grid">
      <li v-for="service in services" :key="service.key">
        <button
          type="button"
          class="gc-service-card"
          :class="{ 'gc-service-card-active': selectedService === service.key }"
          @click="onSelectService(service.key)"
        >
          <span class="gc-service-card-icon" :class="`gc-service-card-icon-${service.key}`">
            <q-icon :name="service.icon" size="22px" />
          </span>
          <span class="gc-service-card-label">
            {{ t(`dashboard.overview.serviceLabels.${service.key}`) }}
          </span>
          <q-icon
            v-if="selectedService === service.key"
            name="check_circle"
            size="18px"
            class="gc-service-card-check"
          />
        </button>
      </li>
    </ul>

    <header class="gc-step-section-header">
      <h3 class="gc-step-section-title">{{ t('dashboard.edit.serviceStep.targetHeading') }}</h3>
      <p class="gc-step-section-sub">{{ t('dashboard.edit.serviceStep.targetSubheading') }}</p>
    </header>

    <div v-if="selectedTargetSlug" class="gc-target-selected">
      <div class="gc-target-selected-content">
        <span class="gc-target-selected-label">
          {{ t('dashboard.edit.serviceStep.currentSelection') }}
        </span>
        <span class="gc-target-selected-name">{{ selectedTargetLabel }}</span>
      </div>
      <q-btn
        flat
        no-caps
        dense
        :label="t('dashboard.edit.serviceStep.clearTarget')"
        class="gc-target-clear"
        @click="onClearTarget"
      />
    </div>

    <div v-else-if="loading" class="gc-target-loading">
      <q-spinner color="primary" size="28px" />
    </div>

    <p v-else-if="catalogItems.length === 0" class="gc-target-empty">
      {{ t('dashboard.edit.serviceStep.catalogEmpty') }}
    </p>

    <ul v-else class="gc-target-grid">
      <li class="gc-target-item">
        <button type="button" class="gc-target-card gc-target-card-skip" @click="onClearTarget">
          <div class="gc-target-card-icon">
            <q-icon name="explore" size="20px" />
          </div>
          <div class="gc-target-card-text">
            <span class="gc-target-card-title">{{ t('dashboard.edit.serviceStep.noTarget') }}</span>
            <span class="gc-target-card-desc">{{
              t('dashboard.edit.serviceStep.noTargetDescription')
            }}</span>
          </div>
        </button>
      </li>

      <li v-for="item in catalogItems" :key="item.slug" class="gc-target-item">
        <button type="button" class="gc-target-card" @click="onSelectTarget(item.slug, item.title)">
          <div class="gc-target-card-cover">
            <img
              v-if="item.cover_image_url"
              :src="item.cover_image_url"
              :alt="item.title"
              loading="lazy"
            />
            <div v-else class="gc-target-card-cover-placeholder"></div>
          </div>
          <div class="gc-target-card-text">
            <span class="gc-target-card-title">{{ item.title }}</span>
            <span class="gc-target-card-desc">{{ item.subtitle }}</span>
          </div>
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import {
  jobsService,
  tourPackagesService,
  universitiesService,
  visaTypesService,
} from 'src/services/catalog';
import type { ServiceType } from 'src/services/applications';

interface Props {
  serviceType: ServiceType;
  targetSlug: string;
  targetLabel: string;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  'update:service-type': [ServiceType];
  'update:target': [{ slug: string; label: string }];
}>();

const { t, locale } = useI18n();

const selectedService = computed(() => props.serviceType);
const selectedTargetSlug = computed(() => props.targetSlug);
const selectedTargetLabel = computed(() => props.targetLabel);

interface CatalogChoice {
  slug: string;
  title: string;
  subtitle: string;
  cover_image_url: string | null;
}

const services = [
  { key: 'tourism' as ServiceType, icon: 'wb_sunny' },
  { key: 'study' as ServiceType, icon: 'menu_book' },
  { key: 'work' as ServiceType, icon: 'business_center' },
  { key: 'visa' as ServiceType, icon: 'description' },
];

const catalogItems = ref<CatalogChoice[]>([]);
const loading = ref(false);

async function loadCatalog() {
  loading.value = true;
  try {
    if (selectedService.value === 'tourism') {
      const items = await tourPackagesService.list();
      catalogItems.value = items.map((it) => ({
        slug: it.slug,
        title: it.title,
        subtitle: it.destination,
        cover_image_url: it.cover_image_url,
      }));
    } else if (selectedService.value === 'study') {
      const items = await universitiesService.list();
      catalogItems.value = items.map((it) => ({
        slug: it.slug,
        title: it.title,
        subtitle: it.city ? `${it.city}, ${it.country}` : it.country,
        cover_image_url: it.cover_image_url,
      }));
    } else if (selectedService.value === 'work') {
      const items = await jobsService.list();
      catalogItems.value = items.map((it) => ({
        slug: it.slug,
        title: it.title,
        subtitle: it.city ? `${it.city}, ${it.country}` : it.country,
        cover_image_url: it.cover_image_url,
      }));
    } else if (selectedService.value === 'visa') {
      const items = await visaTypesService.list();
      catalogItems.value = items.map((it) => ({
        slug: it.slug,
        title: it.title,
        subtitle: it.country,
        cover_image_url: it.cover_image_url,
      }));
    }
  } catch {
    catalogItems.value = [];
  } finally {
    loading.value = false;
  }
}

function onSelectService(value: ServiceType) {
  if (value === selectedService.value) return;
  emit('update:service-type', value);
  emit('update:target', { slug: '', label: '' });
}

function onSelectTarget(slug: string, label: string) {
  emit('update:target', { slug, label });
}

function onClearTarget() {
  emit('update:target', { slug: '', label: '' });
}

onMounted(loadCatalog);
watch(() => props.serviceType, loadCatalog);
watch(locale, loadCatalog);
</script>

<style scoped lang="scss">
.gc-step1 {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.gc-step-section-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.gc-step-section-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
}

.gc-step-section-sub {
  font-size: 13px;
  color: var(--gc-text-muted);
  margin: 0;
}

.gc-service-grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;

  @media (min-width: 720px) {
    grid-template-columns: repeat(4, 1fr);
  }
}

.gc-service-card {
  appearance: none;
  border: 1px solid var(--gc-border);
  background: var(--gc-bg);
  border-radius: var(--gc-radius-md);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  cursor: pointer;
  text-align: left;
  position: relative;
  transition:
    border-color 0.15s ease,
    background 0.15s ease,
    transform 0.15s ease;
  width: 100%;

  &:hover {
    border-color: var(--gc-primary);
  }
}

.gc-service-card-active {
  border-color: var(--gc-primary);
  background: var(--gc-primary-soft);
}

.gc-service-card-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--gc-bg-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gc-primary);
}

.gc-service-card-icon-tourism {
  color: #c97900;
}
.gc-service-card-icon-study {
  color: var(--gc-primary);
}
.gc-service-card-icon-work {
  color: #4a8dff;
}
.gc-service-card-icon-visa {
  color: #d04848;
}

.gc-service-card-label {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.gc-service-card-check {
  position: absolute;
  top: 12px;
  right: 12px;
  color: var(--gc-primary);
}

.gc-target-selected {
  background: var(--gc-primary-soft);
  border: 1px solid var(--gc-primary);
  border-radius: var(--gc-radius-md);
  padding: 14px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.gc-target-selected-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.gc-target-selected-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
  color: var(--gc-primary);
}

.gc-target-selected-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--gc-text);
}

.gc-target-clear {
  color: var(--gc-primary);
  font-weight: 500;
  flex-shrink: 0;
}

.gc-target-loading {
  display: flex;
  justify-content: center;
  padding: 32px 0;
}

.gc-target-empty {
  text-align: center;
  color: var(--gc-text-muted);
  margin: 16px 0;
}

.gc-target-grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;

  @media (min-width: 600px) {
    grid-template-columns: repeat(2, 1fr);
  }
}

.gc-target-item {
  display: block;
}

.gc-target-card {
  appearance: none;
  border: 1px solid var(--gc-border);
  background: var(--gc-bg);
  border-radius: var(--gc-radius-md);
  padding: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  text-align: left;
  cursor: pointer;
  width: 100%;
  transition:
    border-color 0.15s ease,
    transform 0.15s ease;

  &:hover {
    border-color: var(--gc-primary);
    transform: translateY(-1px);
  }
}

.gc-target-card-skip {
  background: var(--gc-bg-soft);
}

.gc-target-card-cover {
  width: 56px;
  height: 56px;
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

.gc-target-card-cover-placeholder {
  width: 100%;
  height: 100%;
  background: var(--gc-bg-soft);
}

.gc-target-card-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--gc-radius-sm);
  background: var(--gc-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gc-primary);
  flex-shrink: 0;
}

.gc-target-card-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.gc-target-card-title {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: -0.01em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.gc-target-card-desc {
  font-size: 12px;
  color: var(--gc-text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
