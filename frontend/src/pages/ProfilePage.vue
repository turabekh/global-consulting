<template>
  <q-page class="gc-profile-page">
    <div class="gc-profile-shell">
      <header class="gc-profile-header">
        <h1 class="gc-h1">{{ t('profile.title') }}</h1>
        <p class="gc-subtitle">{{ authStore.user?.email }}</p>
      </header>

      <section class="gc-profile-card">
        <h2 class="gc-section-title">{{ t('profile.avatar') }}</h2>
        <div class="gc-avatar-row">
          <q-avatar size="80px" class="gc-profile-avatar">
            <img v-if="avatarUrl" :src="avatarUrl" alt="" />
            <span v-else class="gc-avatar-fallback">{{ initials }}</span>
          </q-avatar>
          <q-file
            v-model="avatarFile"
            outlined
            dense
            accept="image/*"
            class="gc-avatar-input"
            :label="t('profile.uploadAvatar')"
            @update:model-value="onAvatarSelected"
          >
            <template #prepend>
              <q-icon name="photo_camera" />
            </template>
          </q-file>
        </div>
      </section>

      <section class="gc-profile-card">
        <h2 class="gc-section-title">{{ t('profile.personalInfo') }}</h2>

        <q-form class="gc-form" @submit.prevent="onSave">
          <div class="gc-grid-2">
            <div class="gc-field">
              <label class="gc-label" for="first_name">{{ t('profile.firstName') }}</label>
              <q-input id="first_name" v-model="firstName" outlined dense />
            </div>
            <div class="gc-field">
              <label class="gc-label" for="last_name">{{ t('profile.lastName') }}</label>
              <q-input id="last_name" v-model="lastName" outlined dense />
            </div>
          </div>

          <div class="gc-field">
            <label class="gc-label" for="phone">{{ t('profile.phone') }}</label>
            <q-input id="phone" v-model="phone" outlined dense placeholder="+998 90 123 45 67" />
          </div>

          <div class="gc-field">
            <label class="gc-label" for="bio">{{ t('profile.bio') }}</label>
            <q-input id="bio" v-model="bio" type="textarea" outlined autogrow />
          </div>

          <div class="gc-field">
            <label class="gc-label" for="language">{{ t('profile.language') }}</label>
            <q-select
              id="language"
              v-model="language"
              :options="languageOptions"
              outlined
              dense
              emit-value
              map-options
            />
          </div>

          <q-banner v-if="error" class="gc-error-banner" dense rounded>{{ error }}</q-banner>

          <q-btn
            type="submit"
            color="primary"
            :loading="authStore.isLoading"
            unelevated
            no-caps
            class="gc-submit-btn"
            :label="t('profile.save')"
          />
        </q-form>
      </section>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useQuasar } from 'quasar';
import { useAuthStore } from 'src/stores/auth';
import { setLocale } from 'src/boot/i18n';
import { extractApiError } from 'src/utils/api-errors';

const { t } = useI18n();
const $q = useQuasar();
const authStore = useAuthStore();

const firstName = ref('');
const lastName = ref('');
const phone = ref('');
const bio = ref('');
const language = ref<string>('en');
const avatarFile = ref<File | null>(null);
const error = ref<string | null>(null);

const languageOptions = [
  { label: 'English', value: 'en' },
  { label: "O'zbek", value: 'uz' },
];

const avatarUrl = computed(() => authStore.user?.profile?.avatar_url ?? null);

const initials = computed(() => {
  const first = authStore.user?.first_name?.[0] ?? '';
  const last = authStore.user?.last_name?.[0] ?? '';
  const fallback = authStore.user?.email?.[0]?.toUpperCase() ?? '?';
  const result = `${first}${last}`.toUpperCase();
  return result || fallback;
});

function syncFromStore() {
  const u = authStore.user;
  if (!u) return;
  firstName.value = u.first_name;
  lastName.value = u.last_name;
  phone.value = u.phone;
  bio.value = u.profile?.bio ?? '';
  language.value = u.profile?.language ?? 'en';
}

watch(() => authStore.user, syncFromStore, { immediate: true });

async function onSave() {
  error.value = null;
  try {
    await authStore.updateProfile({
      first_name: firstName.value,
      last_name: lastName.value,
      phone: phone.value,
      profile: {
        bio: bio.value,
        language: language.value,
      },
    });

    if (language.value === 'en' || language.value === 'uz') {
      setLocale(language.value);
    }

    $q.notify({
      type: 'positive',
      message: t('profile.saved'),
      position: 'top',
      timeout: 2000,
    });
  } catch (err) {
    error.value = extractApiError(err, t('errors.generic'));
  }
}

async function onAvatarSelected(file: File | null) {
  if (!file) return;
  error.value = null;
  try {
    await authStore.uploadAvatar(file);
    $q.notify({
      type: 'positive',
      message: t('profile.saved'),
      position: 'top',
      timeout: 2000,
    });
  } catch (err) {
    error.value = extractApiError(err, t('errors.generic'));
  } finally {
    avatarFile.value = null;
  }
}
</script>

<style scoped lang="scss">
.gc-profile-page {
  background: var(--gc-bg-soft);
  min-height: calc(100vh - 64px);
  padding: 32px 16px 64px;
}

.gc-profile-shell {
  max-width: 720px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.gc-profile-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.gc-profile-card {
  background: var(--gc-bg);
  border-radius: var(--gc-radius-lg);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  box-shadow: var(--gc-shadow-sm);
}

.gc-section-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  letter-spacing: -0.01em;
}

.gc-avatar-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.gc-profile-avatar {
  flex-shrink: 0;
  border: 2px solid var(--gc-border);
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
  font-size: 24px;
}

.gc-avatar-input {
  flex: 1;
  max-width: 360px;
}

.gc-grid-2 {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;

  @media (min-width: 600px) {
    grid-template-columns: 1fr 1fr;
  }
}

.gc-submit-btn {
  border-radius: var(--gc-radius-pill);
  font-weight: 600;
  padding: 8px 24px;
  align-self: flex-start;
}
</style>
