<template>
  <section class="gc-faq">
    <div class="gc-faq-inner">
      <header class="gc-faq-header">
        <h2 class="gc-faq-title">
          {{ t('home.faq.titlePart1') }}
          <span class="gc-gradient-text">{{ t('home.faq.titleHighlight') }}</span>
        </h2>
        <p class="gc-faq-subtitle">
          {{ t('home.faq.subtitle') }}
          <span aria-hidden="true">👋</span>
        </p>
      </header>

      <div class="gc-faq-tabs">
        <button
          v-for="opt in categoryOptions"
          :key="opt.value ?? 'all'"
          type="button"
          class="gc-faq-tab"
          :class="{ 'gc-faq-tab-active': active === opt.value }"
          @click="active = opt.value"
        >
          {{ t(`home.faq.categories.${opt.key}`) }}
        </button>
      </div>

      <div v-if="loading" class="gc-faq-loading">
        <q-spinner color="primary" size="32px" />
      </div>

      <p v-else-if="items.length === 0" class="gc-faq-empty">
        {{ t('home.faq.empty') }}
      </p>

      <ul v-else class="gc-faq-list">
        <li
          v-for="item in items"
          :key="item.id"
          class="gc-faq-item"
          :class="{ 'gc-faq-item-open': openId === item.id }"
        >
          <button
            type="button"
            class="gc-faq-question"
            :aria-expanded="openId === item.id"
            @click="toggle(item.id)"
          >
            <span class="gc-faq-question-text">{{ item.question }}</span>
            <span class="gc-faq-toggle" aria-hidden="true">
              <q-icon :name="openId === item.id ? 'close' : 'add'" size="18px" />
            </span>
          </button>

          <div v-show="openId === item.id" class="gc-faq-answer" v-html="item.answer_html"></div>
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { faqService, type FAQ, type FAQCategory } from 'src/services/faq';

const { t, locale } = useI18n();

const items = ref<FAQ[]>([]);
const loading = ref(true);
const active = ref<FAQCategory | null>(null);
const openId = ref<number | null>(null);

interface CategoryOption {
  key: 'all' | FAQCategory;
  value: FAQCategory | null;
}

const categoryOptions: CategoryOption[] = [
  { key: 'all', value: null },
  { key: 'work', value: 'work' },
  { key: 'study', value: 'study' },
  { key: 'tourism', value: 'tourism' },
  { key: 'visa', value: 'visa' },
];

async function load() {
  loading.value = true;
  try {
    items.value = await faqService.list(active.value ?? undefined);
    openId.value = null;
  } catch {
    items.value = [];
  } finally {
    loading.value = false;
  }
}

function toggle(id: number) {
  openId.value = openId.value === id ? null : id;
}

onMounted(load);
watch([active, locale], load);
</script>

<style scoped lang="scss">
.gc-faq {
  padding: 48px 16px;

  @media (min-width: 720px) {
    padding: 80px 16px;
  }
}

.gc-faq-inner {
  max-width: 1600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.gc-faq-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
  text-align: center;
  align-items: center;
}

.gc-faq-title {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.15;
  margin: 0;

  @media (min-width: 720px) {
    font-size: 36px;
  }
}

.gc-faq-subtitle {
  font-size: 14px;
  color: var(--gc-text-muted);
  margin: 0;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.gc-faq-tabs {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px;
  margin: 8px 0 24px;
}

.gc-faq-tab {
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

.gc-faq-tab-active {
  background: var(--gc-primary);
  color: #ffffff;

  &:hover {
    background: var(--gc-primary);
  }
}

.gc-faq-loading {
  display: flex;
  justify-content: center;
  padding: 32px 0;
}

.gc-faq-empty {
  text-align: center;
  color: var(--gc-text-muted);
  margin: 32px 0;
}

.gc-faq-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gc-faq-item {
  background: var(--gc-bg-soft);
  border-radius: var(--gc-radius-md);
  overflow: hidden;
  transition: background 0.15s ease;
}

.gc-faq-item-open {
  background: var(--gc-bg-soft);
}

.gc-faq-question {
  appearance: none;
  border: none;
  background: transparent;
  cursor: pointer;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 18px 20px;
  text-align: left;
  font-size: 15px;
  font-weight: 600;
  color: var(--gc-text);
  letter-spacing: -0.01em;
}

.gc-faq-question-text {
  flex: 1;
}

.gc-faq-toggle {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--gc-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gc-text);
  transition:
    background 0.15s ease,
    color 0.15s ease;
}

.gc-faq-item-open .gc-faq-toggle {
  background: var(--gc-primary);
  color: #ffffff;
}

.gc-faq-answer {
  padding: 0 20px 20px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--gc-text-muted);

  :deep(p) {
    margin: 0 0 12px;
  }

  :deep(p:last-child) {
    margin: 0;
  }

  :deep(strong) {
    color: var(--gc-text);
    font-weight: 600;
  }

  :deep(ul),
  :deep(ol) {
    margin: 0 0 12px;
    padding-left: 20px;
  }

  :deep(a) {
    color: var(--gc-primary);
    text-decoration: underline;
  }
}
</style>
