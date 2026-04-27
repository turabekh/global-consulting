<template>
  <aside class="gc-dash-sidebar">
    <div class="gc-dash-sidebar-top">
      <router-link to="/" class="gc-dash-brand">
        <span class="gc-logo-mark">G</span>
        <span class="gc-dash-brand-name">{{ t('app.name') }}</span>
      </router-link>

      <nav class="gc-dash-nav">
        <router-link
          v-for="item in navItems"
          :key="item.key"
          :to="item.path"
          class="gc-dash-nav-item"
          :class="{ 'gc-dash-nav-item-active': isActive(item) }"
        >
          <q-icon :name="item.icon" size="18px" />
          <span>{{ t(`dashboard.nav.${item.key}`) }}</span>
          <span
            v-if="item.key === 'messages' && messagingStore.totalUnread > 0"
            class="gc-dash-nav-badge"
          >
            {{ messagingStore.totalUnread }}
          </span>
          <span v-else-if="item.disabled" class="gc-dash-nav-soon">soon</span>
        </router-link>
      </nav>
    </div>

    <div class="gc-dash-sidebar-bottom">
      <router-link to="/profile" class="gc-dash-user">
        <q-avatar size="40px">
          <img v-if="avatarUrl" :src="avatarUrl" alt="" />
          <span v-else class="gc-dash-avatar-fallback">{{ initials }}</span>
        </q-avatar>
        <div class="gc-dash-user-text">
          <span class="gc-dash-user-name">{{ displayName }}</span>
          <span class="gc-dash-user-email">{{ authStore.user?.email }}</span>
        </div>
      </router-link>

      <button type="button" class="gc-dash-signout" @click="onSignOut">
        <q-icon name="logout" size="16px" />
        {{ t('dashboard.nav.signOut') }}
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from 'src/stores/auth';
import { useMessagingStore } from 'src/stores/messaging';

const messagingStore = useMessagingStore();

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

interface NavItem {
  key: 'overview' | 'applications' | 'messages' | 'profile';
  path: string;
  icon: string;
  disabled?: boolean;
  matchPaths?: string[];
}

const navItems: NavItem[] = [
  { key: 'overview', path: '/dashboard', icon: 'space_dashboard' },
  {
    key: 'applications',
    path: '/dashboard/applications',
    icon: 'description',
    matchPaths: ['/dashboard/applications'],
  },
  {
    key: 'messages',
    path: '/dashboard/messages',
    icon: 'forum',
    matchPaths: ['/dashboard/messages'],
  },
  { key: 'profile', path: '/profile', icon: 'person' },
];

function isActive(item: NavItem): boolean {
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

const displayName = computed(() => {
  const u = authStore.user;
  if (!u) return '';
  const full = `${u.first_name ?? ''} ${u.last_name ?? ''}`.trim();
  return full || u.email;
});

async function onSignOut() {
  await authStore.logout();
  await router.push('/');
}
</script>

<style scoped lang="scss">
.gc-dash-sidebar {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 20px 16px;
  background: var(--gc-bg);
  border-right: 1px solid var(--gc-border);
  gap: 24px;
  overflow-y: auto;
}

.gc-dash-sidebar-top {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.gc-dash-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: inherit;
  padding: 4px 8px;
}

.gc-logo-mark {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #c084fc 0%, #ec4899 100%);
  color: #ffffff;
  font-weight: 700;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.gc-dash-brand-name {
  font-weight: 600;
  font-size: 14px;
  letter-spacing: -0.01em;
}

.gc-dash-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.gc-dash-nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: var(--gc-radius-md);
  font-size: 14px;
  font-weight: 500;
  color: var(--gc-text);
  text-decoration: none;
  transition:
    background 0.15s ease,
    color 0.15s ease;

  &:hover {
    background: var(--gc-bg-soft);
  }
}

.gc-dash-nav-item-active {
  background: var(--gc-primary);
  color: #ffffff;

  &:hover {
    background: var(--gc-primary);
  }
}

.gc-dash-nav-soon {
  margin-left: auto;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--gc-text-muted);
  font-weight: 600;
}

.gc-dash-sidebar-bottom {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid var(--gc-border);
}

.gc-dash-user {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: var(--gc-radius-md);
  text-decoration: none;
  color: inherit;

  &:hover {
    background: var(--gc-bg-soft);
  }
}

.gc-dash-avatar-fallback {
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

.gc-dash-user-text {
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 0;
}

.gc-dash-user-name {
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.gc-dash-user-email {
  font-size: 11px;
  color: var(--gc-text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.gc-dash-signout {
  appearance: none;
  border: none;
  background: transparent;
  color: var(--gc-text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: var(--gc-radius-md);
  font-size: 13px;
  font-weight: 500;
  transition:
    background 0.15s ease,
    color 0.15s ease;

  &:hover {
    background: var(--gc-bg-soft);
    color: var(--gc-text);
  }
}

.gc-dash-nav-badge {
  margin-left: auto;
  min-width: 20px;
  height: 20px;
  padding: 0 7px;
  border-radius: 10px;
  background: var(--gc-primary);
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.gc-dash-nav-item-active .gc-dash-nav-badge {
  background: rgba(255, 255, 255, 0.22);
}
</style>
