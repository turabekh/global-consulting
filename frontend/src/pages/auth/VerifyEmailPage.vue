<template>
  <div class="gc-auth-content">
    <router-link to="/login" class="gc-back-link">
      <q-icon name="arrow_back" size="xs" />
      {{ t('common.back') }}
    </router-link>

    <div v-if="status === 'verifying'" class="gc-verify-status">
      <q-spinner-dots color="primary" size="48px" />
      <p class="gc-subtitle">{{ t('auth.verifyEmail.verifying') }}</p>
    </div>

    <AuthSuccessCard
      v-else-if="status === 'success'"
      icon="check"
      :title="t('auth.verifyEmail.successTitle')"
      :message="t('auth.verifyEmail.successMessage')"
      :action-label="t('auth.verifyEmail.successAction')"
      @action="goToLogin"
    />

    <div v-else class="gc-auth-content">
      <div class="gc-auth-title">
        <h1 class="gc-h1">{{ t('auth.verifyEmail.title') }}</h1>
        <p class="gc-subtitle">{{ t('auth.verifyEmail.message') }}</p>
      </div>

      <q-form class="gc-form" @submit.prevent="onSubmit">
        <div class="gc-field">
          <label class="gc-label" for="code">{{ t('auth.verifyEmail.code') }}</label>
          <q-input
            id="code"
            v-model="code"
            outlined
            dense
            placeholder=""
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
          :label="t('auth.verifyEmail.submit')"
        />
      </q-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from 'src/stores/auth';
import { extractApiError } from 'src/utils/api-errors';
import AuthSuccessCard from 'src/components/AuthSuccessCard.vue';

type Status = 'idle' | 'verifying' | 'success';

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const code = ref('');
const error = ref<string | null>(null);
const loading = ref(false);
const status = ref<Status>('idle');

async function verify(key: string) {
  status.value = 'verifying';
  error.value = null;
  try {
    await authStore.verifyEmail({ key });
    status.value = 'success';
  } catch (err) {
    status.value = 'idle';
    error.value = extractApiError(err, t('errors.generic'));
  }
}

async function onSubmit() {
  loading.value = true;
  await verify(code.value);
  loading.value = false;
}

function goToLogin() {
  void router.push('/login');
}

onMounted(() => {
  const key = route.params.key;
  if (typeof key === 'string' && key.length > 0) {
    void verify(key);
  }
});
</script>

<style scoped lang="scss">
.gc-verify-status {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 48px 0;
}
</style>
