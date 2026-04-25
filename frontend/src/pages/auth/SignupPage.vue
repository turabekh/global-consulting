<template>
  <div v-if="!signedUp" class="gc-auth-content">
    <div class="gc-auth-title">
      <h1 class="gc-h1">{{ t('auth.signup.title') }}</h1>
      <p class="gc-subtitle">{{ t('auth.signup.subtitle') }}</p>
    </div>

    <q-form class="gc-form" @submit.prevent="onSubmit">
      <div class="gc-field">
        <label class="gc-label" for="email">{{ t('auth.signup.email') }}</label>
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

      <div class="gc-field">
        <label class="gc-label" for="password">{{ t('auth.signup.password') }}</label>
        <q-input
          id="password"
          v-model="password1"
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
        <label class="gc-label" for="password2">{{ t('auth.signup.confirmPassword') }}</label>
        <q-input
          id="password2"
          v-model="password2"
          :type="showPassword2 ? 'text' : 'password'"
          outlined
          dense
          placeholder="••••••••"
          :rules="[
            (v) => !!v || t('errors.required'),
            (v) => v === password1 || t('errors.passwordMismatch'),
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
        :loading="authStore.isLoading"
        unelevated
        no-caps
        size="md"
        class="gc-submit-btn full-width"
        :label="t('auth.signup.submit')"
      />

      <div class="gc-divider">
        <span>{{ t('auth.login.or') }}</span>
      </div>

      <div class="gc-social">
        <q-btn
          outline
          no-caps
          class="gc-social-btn"
          icon="img:https://www.google.com/favicon.ico"
          :label="t('auth.login.continueWithGoogle')"
          :loading="socialLoading === 'google'"
          :disable="socialLoading !== null"
          @click="onSocialLogin('google')"
        />
        <q-btn
          outline
          no-caps
          class="gc-social-btn"
          icon="facebook"
          :label="t('auth.login.continueWithFacebook')"
          :loading="socialLoading === 'facebook'"
          :disable="socialLoading !== null"
          @click="onSocialLogin('facebook')"
        />
      </div>

      <p class="gc-foot">
        {{ t('auth.signup.hasAccount') }}
        <router-link to="/login" class="gc-link gc-link-strong">
          {{ t('auth.signup.login') }}
        </router-link>
      </p>
    </q-form>
  </div>

  <AuthSuccessCard
    v-else
    icon="mark_email_read"
    :title="t('auth.signup.successTitle')"
    :message="t('auth.signup.successMessage', { email })"
    :action-label="t('auth.signup.successAction')"
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
const password1 = ref('');
const password2 = ref('');
const showPassword = ref(false);
const showPassword2 = ref(false);
const error = ref<string | null>(null);
const signedUp = ref(false);
const socialLoading = ref<'google' | 'facebook' | null>(null);

async function onSocialLogin(provider: 'google' | 'facebook') {
  error.value = null;
  socialLoading.value = provider;
  try {
    if (provider === 'google') {
      await authStore.loginWithGoogle();
    } else {
      await authStore.loginWithFacebook();
    }
    await router.push('/');
  } catch (err) {
    error.value = extractApiError(err, t('errors.generic'));
  } finally {
    socialLoading.value = null;
  }
}

async function onSubmit() {
  error.value = null;
  try {
    await authStore.signup({
      email: email.value,
      password1: password1.value,
      password2: password2.value,
    });
    signedUp.value = true;
  } catch (err) {
    error.value = extractApiError(err, t('errors.generic'));
  }
}

function goToLogin() {
  void router.push('/login');
}
</script>
