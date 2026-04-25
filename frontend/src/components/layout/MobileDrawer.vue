<template>
  <q-drawer v-model="open" side="right" overlay behavior="mobile" :width="320">
    <div class="gc-mobile-drawer">
      <div class="gc-mobile-drawer-head">
        <span class="gc-logo-mark">G</span>
        <q-btn flat round dense icon="close" @click="open = false" />
      </div>

      <nav class="gc-mobile-nav">
        <router-link
          v-for="item in navItems"
          :key="item.key"
          :to="item.path"
          class="gc-mobile-nav-item"
          :class="{ 'gc-mobile-nav-item-active': isActive(item) }"
          @click="open = false"
        >
          <span>{{ t(`nav.${item.key}`) }}</span>
          <q-icon name="chevron_right" size="18px" />
        </router-link>
      </nav>

      <div class="gc-mobile-divider"></div>

      <div class="gc-mobile-section">
        <div class="gc-mobile-section-label">{{ t('profile.language') }}</div>
        <div class="gc-mobile-locale-row">
          <button
            v-for="opt in localeOptions"
            :key="opt.value"
            type="button"
            class="gc-mobile-locale-pill"
            :class="{ 'gc-mobile-locale-pill-active': locale === opt.value }"
            @click="onChangeLocale(opt.value)"
          >
            {{ opt.label }}
          </button>
        </div>
      </div>

      <div class="gc-mobile-spacer"></div>

      <div class="gc-mobile-foot">
        <template v-if="authStore.isAuthenticated">
          <router-link to="/profile" class="gc-mobile-user" @click="open = false">
            <q-avatar size="40px">
              <img v-if="avatarUrl" :src="avatarUrl" alt="" />
              <span v-else class="gc-avatar-fallback">{{ initials }}</span>
            </q-avatar>
            <div class="gc-mobile-user-text">
              <span class="gc-mobile-user-name">{{
                authStore.user?.full_name || authStore.user?.email
              }}</span>
              <span class="gc-mobile-user-meta">{{ t('profile.title') }}</span>
            </div>
          </router-link>
          <q-btn
            flat
            no-caps
            icon="logout"
            :label="t('profile.logout')"
            class="gc-mobile-logout"
            @click="onMobileLogout"
          />
        </template>
        <template v-else>
          <q-btn
            outline
            no-caps
            :label="t('nav.logIn')"
            class="gc-mobile-cta gc-mobile-cta-secondary"
            to="/login"
            @click="open = false"
          />
          <q-btn
            color="dark"
            unelevated
            no-caps
            :label="t('nav.signUp')"
            class="gc-mobile-cta"
            to="/signup"
            @click="open = false"
          />
        </template>
      </div>
    </div>
  </q-drawer>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from 'src/stores/auth';
import { setLocale } from 'src/boot/i18n';
import type { SupportedLocale } from 'src/i18n';

const open = defineModel<boolean>({ required: true });

const { t, locale } = useI18n();
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

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

async function onMobileLogout() {
  open.value = false;
  await authStore.logout();
  await router.push('/');
}
</script>

<style scoped lang="scss">
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
