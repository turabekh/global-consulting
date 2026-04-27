<template>
  <header class="gc-site-header">
    <div class="gc-header-inner">
      <router-link to="/" class="gc-brand">
        <span class="gc-logo-mark">G</span>
      </router-link>

      <nav class="gc-nav-pill">
        <router-link
          v-for="item in navItems"
          :key="item.key"
          :to="item.path"
          class="gc-nav-item"
          :class="{ 'gc-nav-item-active': isActive(item) }"
        >
          {{ t(`nav.${item.key}`) }}
          <q-icon v-if="item.key === 'services'" name="expand_more" size="14px" />
          <ServicesMenu v-if="item.key === 'services'" />
        </router-link>
      </nav>

      <div class="gc-header-actions">
        <q-btn flat round dense icon="language" class="gc-icon-btn" aria-label="Change language">
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

        <template v-if="authStore.isAuthenticated">
          <q-btn
            unelevated
            no-caps
            dense
            color="primary"
            :label="t('nav.dashboard')"
            to="/dashboard"
            class="gc-header-dashboard-btn"
          >
            <span v-if="messagingStore.totalUnread > 0" class="gc-header-dashboard-badge">
              {{ messagingStore.totalUnread }}
            </span>
          </q-btn>
          <q-btn flat round dense class="gc-avatar-btn" aria-label="User menu">
            <q-avatar size="32px">
              <img v-if="avatarUrl" :src="avatarUrl" alt="" />
              <span v-else class="gc-avatar-fallback">{{ initials }}</span>
            </q-avatar>
            <q-menu anchor="bottom right" self="top right" :offset="[0, 8]">
              <q-list style="min-width: 200px">
                <q-item-label header>{{ authStore.user?.email }}</q-item-label>
                <q-item v-close-popup clickable to="/profile">
                  <q-item-section avatar>
                    <q-icon name="person" size="18px" />
                  </q-item-section>
                  <q-item-section>{{ t('profile.title') }}</q-item-section>
                </q-item>
                <q-separator />

                <q-item v-close-popup clickable to="/dashboard">
                  <q-item-section avatar>
                    <q-icon name="space_dashboard" size="18px" />
                  </q-item-section>
                  <q-item-section>{{ t('nav.dashboard') }}</q-item-section>
                </q-item>

                <q-item v-close-popup clickable to="/profile">
                  <q-item-section avatar>
                    <q-icon name="person" size="18px" />
                  </q-item-section>
                  <q-item-section>{{ t('profile.title') }}</q-item-section>
                </q-item>
                <q-item v-close-popup clickable @click="onLogout">
                  <q-item-section avatar>
                    <q-icon name="logout" size="18px" />
                  </q-item-section>
                  <q-item-section>{{ t('profile.logout') }}</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </template>

        <template v-else>
          <q-btn flat no-caps dense :label="t('nav.logIn')" class="gc-login-btn" to="/login" />
          <q-btn
            color="dark"
            unelevated
            no-caps
            :label="t('nav.signUp')"
            class="gc-signup-btn"
            to="/signup"
          />
        </template>
        <q-btn
          flat
          round
          dense
          icon="menu"
          class="gc-mobile-menu-btn"
          aria-label="Menu"
          @click="emit('open-mobile-menu')"
        />
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from 'src/stores/auth';
import { setLocale } from 'src/boot/i18n';
import type { SupportedLocale } from 'src/i18n';
import ServicesMenu from './ServicesMenu.vue';
import { useMessagingStore } from 'src/stores/messaging';

const { t, locale } = useI18n();
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const messagingStore = useMessagingStore();
const emit = defineEmits<{ 'open-mobile-menu': [] }>();

interface NavItem {
  key: 'home' | 'services' | 'about' | 'testimonial' | 'contact' | 'blog' | 'partnership';
  path: string;
  matchPaths?: string[];
}

const navItems: NavItem[] = [
  { key: 'home', path: '/' },
  { key: 'services', path: '/services', matchPaths: ['/services'] },
  { key: 'about', path: '/about' },
  { key: 'testimonial', path: '/testimonial' },
  { key: 'contact', path: '/contact' },
  { key: 'blog', path: '/blog' },
  { key: 'partnership', path: '/partnership' },
];

const localeOptions: { label: string; value: SupportedLocale }[] = [
  { label: 'English', value: 'en' },
  { label: "O'zbek", value: 'uz' },
];

function isActive(item: NavItem): boolean {
  if (item.path === '/') {
    return route.path === '/';
  }
  if (item.matchPaths?.some((p) => route.path.startsWith(p))) {
    return true;
  }
  return route.path === item.path;
}

const avatarUrl = computed(() => authStore.user?.profile?.avatar_url ?? null);

const initials = computed(() => {
  const first = authStore.user?.first_name?.[0] ?? '';
  const last = authStore.user?.last_name?.[0] ?? '';
  const fallback = authStore.user?.email?.[0]?.toUpperCase() ?? '?';
  const result = `${first}${last}`.toUpperCase();
  return result || fallback;
});

function onChangeLocale(value: SupportedLocale) {
  setLocale(value);
}

async function onLogout() {
  await authStore.logout();
  await router.push('/');
}
</script>

<style scoped lang="scss">
.gc-site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(243, 239, 239, 0.85);
  backdrop-filter: saturate(180%) blur(12px);
  -webkit-backdrop-filter: saturate(180%) blur(12px);
  border-bottom: 1px solid rgba(229, 231, 235, 0.6);
}

.gc-header-inner {
  width: 100%;
  margin: 0;
  padding: 12px 32px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.gc-brand {
  text-decoration: none;
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.gc-logo-mark {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #c084fc 0%, #ec4899 100%);
  color: #ffffff;
  font-weight: 700;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  letter-spacing: -0.02em;
}

.gc-nav-pill {
  display: none;
  margin-left: 24px;
  padding: 6px;
  background: transparent;

  @media (min-width: 1024px) {
    display: flex;
    align-items: center;
    gap: 4px;
  }
}

.gc-nav-item {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 8px 14px;
  border-radius: var(--gc-radius-pill);
  font-size: 14px;
  font-weight: 500;
  color: var(--gc-text);
  text-decoration: none;
  transition: background 0.15s ease;

  &:hover {
    background: var(--gc-bg-soft);
  }
}

.gc-nav-item-active {
  background: var(--gc-bg-soft);
  font-weight: 600;
}

.gc-header-actions {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-left: auto;
}

.gc-icon-btn {
  color: var(--gc-text);
}

.gc-avatar-btn {
  margin-left: 4px;
}

.gc-avatar-fallback {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gc-primary-soft);
  color: var(--gc-primary);
  font-weight: 600;
  font-size: 13px;
}

.gc-signup-btn {
  border-radius: var(--gc-radius-pill);
  padding: 6px 16px;
  font-weight: 500;
  margin-left: 8px;
}

.gc-header-dashboard-btn {
  border-radius: var(--gc-radius-pill);
  padding: 6px 16px;
  font-weight: 600;
  font-size: 13px;
  position: relative;
  margin-right: 4px;
}

.gc-header-dashboard-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 9px;
  background: #d04848;
  color: #ffffff;
  font-size: 10px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.gc-header-dashboard-btn {
  border-radius: var(--gc-radius-pill);
  padding: 6px 16px;
  font-weight: 600;
  font-size: 13px;
  position: relative;
  margin-right: 4px;
  display: none;

  @media (min-width: 720px) {
    display: inline-flex;
  }
}

.gc-mobile-menu-btn {
  margin-left: 4px;

  @media (min-width: 1024px) {
    display: none;
  }
}

.gc-mobile-drawer {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.gc-mobile-drawer-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  border-bottom: 1px solid var(--gc-border);
}

.gc-mobile-drawer {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--gc-bg);
}

.gc-mobile-drawer-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
}

.gc-mobile-nav {
  display: flex;
  flex-direction: column;
  padding: 8px 12px;
}

.gc-mobile-nav-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 12px;
  border-radius: var(--gc-radius-md);
  font-size: 15px;
  font-weight: 500;
  color: var(--gc-text);
  text-decoration: none;

  &:hover,
  &:focus-visible {
    background: var(--gc-bg-soft);
  }
}

.gc-mobile-nav-item-active {
  background: var(--gc-bg-soft);
  color: var(--gc-primary);
  font-weight: 600;
}

.gc-mobile-divider {
  height: 1px;
  background: var(--gc-border);
  margin: 8px 20px;
}

.gc-mobile-section {
  padding: 8px 20px 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.gc-mobile-section-label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gc-text-muted);
}

.gc-mobile-locale-row {
  display: flex;
  gap: 8px;
}

.gc-mobile-locale-pill {
  appearance: none;
  border: 1px solid var(--gc-border);
  background: var(--gc-bg);
  color: var(--gc-text);
  border-radius: var(--gc-radius-pill);
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition:
    background 0.15s ease,
    border-color 0.15s ease,
    color 0.15s ease;

  &:hover {
    background: var(--gc-bg-soft);
  }
}

.gc-mobile-locale-pill-active {
  background: var(--gc-primary);
  border-color: var(--gc-primary);
  color: #ffffff;
}

.gc-mobile-spacer {
  flex: 1;
}

.gc-mobile-foot {
  padding: 16px 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-top: 1px solid var(--gc-border);
}

.gc-mobile-user {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  border-radius: var(--gc-radius-md);
  text-decoration: none;
  color: inherit;

  &:hover {
    background: var(--gc-bg-soft);
  }
}

.gc-mobile-user-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.gc-mobile-user-name {
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.gc-mobile-user-meta {
  font-size: 12px;
  color: var(--gc-text-muted);
}

.gc-mobile-logout {
  justify-content: flex-start;
  padding: 10px 12px;
  border-radius: var(--gc-radius-md);
  color: var(--gc-text);

  :deep(.q-icon) {
    margin-right: 8px;
  }
}

.gc-mobile-cta {
  border-radius: var(--gc-radius-pill);
  padding: 8px 0;
  font-weight: 500;
}

.gc-mobile-cta-secondary {
  color: var(--gc-text);
  border-color: var(--gc-border);
}
</style>
