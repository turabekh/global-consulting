<template>
  <div v-if="!sent" class="gc-auth-content">
    <router-link to="/login" class="gc-back-link">
      <q-icon name="arrow_back" size="xs" />
      {{ t('common.back') }}
    </router-link>

    <div class="gc-auth-title">
      <h1 class="gc-h1">{{ t('auth.resetPassword.title') }}</h1>
      <p class="gc-subtitle">{{ t('auth.resetPassword.message') }}</p>
    </div>

    <q-form class="gc-form" @submit.prevent="onSubmit">
      <div class="gc-field">
        <label class="gc-label" for="email">{{ t('auth.resetPassword.email') }}</label>
        <q-input
          id="email"
          v-model="email"
          type="email"
          outlined
          dense
          placeholder="name@example.com"
          :rules="[(v) => !!v || t('errors.required')]"
          lazy-rules
        />
      </div>

      <q-banner v-if="error" class="gc-error-banner" dense rounded>
        {{ error }}
      </q-banner>

      <q-btn
        type="submit"
        color="primary"
        :loading="loading"
        unelevated
        no-caps
        size="md"
        class="gc-submit-btn full-width"
        :label="t('auth.resetPassword.submit')"
      />
    </q-form>
  </div>

  <AuthSuccessCard
    v-else
    icon="mark_email_read"
    :title="t('auth.resetPassword.successTitle')"
    :message="t('auth.resetPassword.successMessage', { email })"
    :action-label="t('auth.resetPassword.successAction')"
    @action="goToLogin"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import { useAuthStore } from 'src/stores/auth';
import { extractApiError } from 'src/utils/api-errors';
import AuthSuccessCard from 'src/components/AuthSuccessCard.vue';

const { t } = useI18n();
const router = useRouter();
const authStore = useAuthStore();

const email = ref('');
const error = ref<string | null>(null);
const loading = ref(false);
const sent = ref(false);

async function onSubmit() {
  loading.value = true;
  error.value = null;
  try {
    await authStore.requestPasswordReset({ email: email.value });
    sent.value = true;
  } catch (err) {
    error.value = extractApiError(err, t('errors.generic'));
  } finally {
    loading.value = false;
  }
}

function goToLogin() {
  void router.push('/login');
}
</script>
