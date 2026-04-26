<template>
  <header class="gc-dash-topbar">
    <div class="gc-dash-topbar-left">
      <q-btn
        flat
        round
        dense
        icon="menu"
        class="gc-dash-mobile-menu-btn"
        aria-label="Menu"
        @click="emit('open-mobile-menu')"
      />
      <slot name="title">
        <h1 class="gc-dash-page-title">{{ title }}</h1>
      </slot>
    </div>

    <div class="gc-dash-topbar-actions">
      <q-btn flat round dense icon="language" class="gc-dash-icon-btn" aria-label="Change language">
        <q-menu anchor="bottom right" self="top right" :offset="[0, 8]">
          <q-list dense style="min-width: 140px">
            <q-item
              v-for="opt in localeOptions"
              :key="opt.value"
              v-close-popup
              clickable
              :active="locale === opt.value"
              @click="onChangeLocale(opt.value)"
            >
              <q-item-section>{{ opt.label }}</q-item-section>
              <q-item-section v-if="locale === opt.value" side>
                <q-icon name="check" size="16px" color="primary" />
              </q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { setLocale } from 'src/boot/i18n';
import type { SupportedLocale } from 'src/i18n';

defineProps<{
  title?: string;
}>();

const emit = defineEmits<{ 'open-mobile-menu': [] }>();

const { locale } = useI18n();

const localeOptions: { label: string; value: SupportedLocale }[] = [
  { label: 'English', value: 'en' },
  { label: "O'zbek", value: 'uz' },
];

function onChangeLocale(value: SupportedLocale) {
  setLocale(value);
}
</script>

<style scoped lang="scss">
.gc-dash-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 16px 24px;
  background: var(--gc-bg);
  border-bottom: 1px solid var(--gc-border);

  @media (min-width: 720px) {
    padding: 16px 32px;
  }
}

.gc-dash-topbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.gc-dash-page-title {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.01em;
  margin: 0;
  color: var(--gc-text);

  @media (min-width: 720px) {
    font-size: 24px;
  }
}

.gc-dash-mobile-menu-btn {
  color: var(--gc-text);

  @media (min-width: 1024px) {
    display: none;
  }
}

.gc-dash-topbar-actions {
  display: flex;
  align-items: center;
  gap: 4px;
}

.gc-dash-icon-btn {
  color: var(--gc-text);
}
</style>
