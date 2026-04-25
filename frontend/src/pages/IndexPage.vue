<template>
  <q-page class="row items-center justify-evenly">
    <div class="column items-center q-gutter-md">
      <h3>{{ t('app.name') }}</h3>

      <div v-if="!authStore.isInitialized">
        <q-spinner />
        <span>{{ t('common.loading') }}</span>
      </div>

      <div v-else-if="authStore.isAuthenticated">
        <p>Logged in as: {{ authStore.user?.email }}</p>
        <p>Verified: {{ authStore.user?.is_email_verified ? 'yes' : 'no' }}</p>
        <q-btn label="Logout" color="negative" @click="onLogout" />
      </div>

      <div v-else>
        <p>Not logged in</p>
      </div>

      <q-separator />

      <q-btn-group>
        <q-btn
          label="EN"
          :color="locale === 'en' ? 'primary' : 'grey'"
          @click="switchLocale('en')"
        />
        <q-btn
          label="UZ"
          :color="locale === 'uz' ? 'primary' : 'grey'"
          @click="switchLocale('uz')"
        />
      </q-btn-group>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { setLocale } from 'src/boot/i18n';
import { useAuthStore } from 'src/stores/auth';
import type { SupportedLocale } from 'src/i18n';

const { t, locale } = useI18n();
const authStore = useAuthStore();

function switchLocale(newLocale: SupportedLocale) {
  setLocale(newLocale);
}

async function onLogout() {
  await authStore.logout();
}
</script>
