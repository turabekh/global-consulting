<template>
  <div class="gc-auth-content">
    <div class="gc-auth-title">
      <h1 class="gc-h1">{{ t('auth.login.title') }}</h1>
      <p class="gc-subtitle">{{ t('auth.login.subtitle') }}</p>
    </div>

    <q-form class="gc-form" @submit.prevent="onSubmit">
      <div class="gc-field">
        <label class="gc-label" for="email">{{ t('auth.login.email') }}</label>
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
        <label class="gc-label" for="password">{{ t('auth.login.password') }}</label>
        <q-input
          id="password"
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          outlined
          dense
          placeholder="••••••••"
          :rules="[(v) => !!v || t('errors.required')]"
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
        <div class="gc-forgot">
          <router-link to="/forgot-password" class="gc-link">
            {{ t('auth.login.forgotPassword') }}
          </router-link>
        </div>
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
        :label="t('auth.login.submit')"
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
          disable
        />
        <q-btn
          outline
          no-caps
          class="gc-social-btn"
          icon="facebook"
          :label="t('auth.login.continueWithFacebook')"
          disable
        />
      </div>

      <p class="gc-foot">
        {{ t('auth.login.noAccount') }}
        <router-link to="/signup" class="gc-link gc-link-strong">
          {{ t('auth.login.signUp') }}
        </router-link>
      </p>
    </q-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import { AxiosError } from 'axios';
import { useAuthStore } from 'src/stores/auth';

const { t } = useI18n();
const router = useRouter();
const authStore = useAuthStore();

const email = ref('');
const password = ref('');
const showPassword = ref(false);
const error = ref<string | null>(null);

async function onSubmit() {
  error.value = null;
  try {
    await authStore.login({ email: email.value, password: password.value });
    await router.push('/');
  } catch (err) {
    if (err instanceof AxiosError && err.response?.data) {
      const data = err.response.data as { non_field_errors?: string[]; detail?: string };
      error.value = data.non_field_errors?.[0] || data.detail || t('errors.generic');
    } else {
      error.value = t('errors.generic');
    }
  }
}
</script>

<style scoped lang="scss">
.gc-auth-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.gc-auth-title {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.gc-h1 {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.02em;
  margin: 0;
}

.gc-subtitle {
  font-size: 14px;
  color: var(--gc-text-muted);
  margin: 0;
}

.gc-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.gc-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.gc-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--gc-text);
}

.gc-forgot {
  display: flex;
  justify-content: flex-end;
  margin-top: -8px;
}

.gc-link {
  color: var(--gc-primary);
  font-size: 13px;
  text-decoration: none;
  font-weight: 500;

  &:hover {
    text-decoration: underline;
  }
}

.gc-link-strong {
  font-weight: 600;
}

.gc-error-banner {
  background: #fee2e2;
  color: #991b1b;
  font-size: 13px;
  border-radius: var(--gc-radius-sm);
}

.gc-submit-btn {
  border-radius: var(--gc-radius-pill);
  font-weight: 600;
  padding: 8px 0;
}

.gc-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--gc-text-muted);
  font-size: 12px;

  &::before,
  &::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--gc-border);
  }
}

.gc-social {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.gc-social-btn {
  border-radius: var(--gc-radius-pill);
  border-color: var(--gc-border);
  color: var(--gc-text);
  font-weight: 500;
}

.gc-foot {
  text-align: center;
  font-size: 13px;
  color: var(--gc-text-muted);
  margin: 8px 0 0;
}
</style>
