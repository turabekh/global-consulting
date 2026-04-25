<template>
  <div v-if="!done" class="gc-auth-content">
    <router-link to="/login" class="gc-back-link">
      <q-icon name="arrow_back" size="xs" />
      {{ t('common.back') }}
    </router-link>

    <div class="gc-auth-title">
      <h1 class="gc-h1">{{ t('auth.setNewPassword.title') }}</h1>
      <p class="gc-subtitle">{{ t('auth.setNewPassword.message') }}</p>
    </div>

    <q-form class="gc-form" @submit.prevent="onSubmit">
      <div class="gc-field">
        <label class="gc-label" for="newPassword">
          {{ t('auth.setNewPassword.newPassword') }}
        </label>
        <q-input
          id="newPassword"
          v-model="newPassword1"
          :type="showPassword ? 'text' : 'password'"
          outlined
          dense
          placeholder="••••••••"
          :rules="[
            (v) => !!v || t('errors.required'),
            (v) => v.length >= 8 || t('errors.passwordTooShort'),
          ]"
          lazy-rules
        >
          <template #append>
            <q-icon
              :name="showPassword ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="showPassword = !showPassword"
            />
          </template>
        </q-input>
      </div>

      <div class="gc-field">
        <label class="gc-label" for="confirmPassword">
          {{ t('auth.setNewPassword.confirmPassword') }}
        </label>
        <q-input
          id="confirmPassword"
          v-model="newPassword2"
          :type="showPassword2 ? 'text' : 'password'"
          outlined
          dense
          placeholder="••••••••"
          :rules="[
            (v) => !!v || t('errors.required'),
            (v) => v === newPassword1 || t('errors.passwordMismatch'),
          ]"
          lazy-rules
        >
          <template #append>
            <q-icon
              :name="showPassword2 ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="showPassword2 = !showPassword2"
            />
          </template>
        </q-input>
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
        :label="t('auth.setNewPassword.submit')"
      />
    </q-form>
  </div>

  <AuthSuccessCard
    v-else
    icon="lock"
    :title="t('auth.setNewPassword.successTitle')"
    :message="t('auth.setNewPassword.successMessage')"
    :action-label="t('auth.setNewPassword.successAction')"
    @action="goToLogin"
  />
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from 'src/stores/auth';
import { extractApiError } from 'src/utils/api-errors';
import AuthSuccessCard from 'src/components/AuthSuccessCard.vue';

const { t } = useI18n();
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const newPassword1 = ref('');
const newPassword2 = ref('');
const showPassword = ref(false);
const showPassword2 = ref(false);
const error = ref<string | null>(null);
const loading = ref(false);
const done = ref(false);

const uid = computed(() => String(route.params.uid ?? ''));
const token = computed(() => String(route.params.token ?? ''));

async function onSubmit() {
  if (!uid.value || !token.value) {
    error.value = t('auth.setNewPassword.invalidLink');
    return;
  }
  loading.value = true;
  error.value = null;
  try {
    await authStore.confirmPasswordReset({
      uid: uid.value,
      token: token.value,
      new_password1: newPassword1.value,
      new_password2: newPassword2.value,
    });
    done.value = true;
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
