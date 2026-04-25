<template>
  <q-layout view="hHh lpr fFf">
    <q-header class="gc-header" bordered>
      <q-toolbar class="gc-toolbar">
        <router-link to="/" class="gc-brand">
          <span class="gc-logo-mark">G</span>
          <span class="gc-brand-name">{{ t('app.name') }}</span>
        </router-link>

        <q-space />

        <q-btn
          flat
          dense
          no-caps
          :label="locale.toUpperCase()"
          icon="language"
          class="gc-locale-toggle"
          @click="toggleLocale"
        />

        <template v-if="authStore.isAuthenticated">
          <q-btn flat round dense class="gc-avatar-btn">
            <q-avatar size="32px">
              <img v-if="avatarUrl" :src="avatarUrl" alt="" />
              <span v-else class="gc-avatar-fallback">{{ initials }}</span>
            </q-avatar>
            <q-menu>
              <q-list style="min-width: 180px">
                <q-item-label header>{{ authStore.user?.email }}</q-item-label>
                <q-item v-close-popup clickable to="/profile">
                  <q-item-section avatar>
                    <q-icon name="person" />
                  </q-item-section>
                  <q-item-section>{{ t('profile.title') }}</q-item-section>
                </q-item>
                <q-separator />
                <q-item v-close-popup clickable @click="onLogout">
                  <q-item-section avatar>
                    <q-icon name="logout" />
                  </q-item-section>
                  <q-item-section>{{ t('profile.logout') }}</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </template>

        <template v-else>
          <q-btn flat no-caps dense to="/login" :label="t('auth.login.title')" />
          <q-btn
            color="primary"
            unelevated
            no-caps
            dense
            to="/signup"
            :label="t('auth.signup.title')"
            class="gc-signup-btn"
          />
        </template>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import { useAuthStore } from 'src/stores/auth';
import { setLocale } from 'src/boot/i18n';

const { t, locale } = useI18n();
const router = useRouter();
const authStore = useAuthStore();

const avatarUrl = computed(() => authStore.user?.profile?.avatar_url ?? null);

const initials = computed(() => {
  const first = authStore.user?.first_name?.[0] ?? '';
  const last = authStore.user?.last_name?.[0] ?? '';
  const fallback = authStore.user?.email?.[0]?.toUpperCase() ?? '?';
  const result = `${first}${last}`.toUpperCase();
  return result || fallback;
});

function toggleLocale() {
  setLocale(locale.value === 'en' ? 'uz' : 'en');
}

async function onLogout() {
  await authStore.logout();
  await router.push('/');
}
</script>

<style scoped lang="scss">
.gc-header {
  background: var(--gc-bg);
  color: var(--gc-text);
}

.gc-toolbar {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  gap: 8px;
}

.gc-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: inherit;
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

.gc-brand-name {
  font-weight: 600;
  font-size: 15px;
  letter-spacing: -0.01em;
}

.gc-locale-toggle {
  font-weight: 500;
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
  padding: 4px 16px;
}
</style>
