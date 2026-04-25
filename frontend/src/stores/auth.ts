import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import {
  authService,
  type LoginPayload,
  type PasswordResetConfirmPayload,
  type PasswordResetPayload,
  type SignupPayload,
  type User,
  type VerifyEmailPayload,
} from 'src/services/auth';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const isInitialized = ref(false);
  const isLoading = ref(false);

  const isAuthenticated = computed(() => user.value !== null);

  async function initialize(): Promise<void> {
    if (isInitialized.value) return;
    isLoading.value = true;
    try {
      user.value = await authService.fetchUser();
    } catch {
      user.value = null;
    } finally {
      isInitialized.value = true;
      isLoading.value = false;
    }
  }

  async function login(payload: LoginPayload): Promise<void> {
    isLoading.value = true;
    try {
      const response = await authService.login(payload);
      user.value = response.user;
    } finally {
      isLoading.value = false;
    }
  }

  async function signup(payload: SignupPayload): Promise<{ detail: string }> {
    isLoading.value = true;
    try {
      return await authService.signup(payload);
    } finally {
      isLoading.value = false;
    }
  }

  async function logout(): Promise<void> {
    isLoading.value = true;
    try {
      await authService.logout();
    } finally {
      user.value = null;
      isLoading.value = false;
    }
  }

  async function verifyEmail(payload: VerifyEmailPayload): Promise<{ detail: string }> {
    return await authService.verifyEmail(payload);
  }

  async function requestPasswordReset(payload: PasswordResetPayload): Promise<{ detail: string }> {
    return await authService.requestPasswordReset(payload);
  }

  async function confirmPasswordReset(
    payload: PasswordResetConfirmPayload,
  ): Promise<{ detail: string }> {
    return await authService.confirmPasswordReset(payload);
  }

  async function refreshUser(): Promise<void> {
    user.value = await authService.fetchUser();
  }

  return {
    user,
    isInitialized,
    isLoading,
    isAuthenticated,
    initialize,
    login,
    signup,
    logout,
    verifyEmail,
    requestPasswordReset,
    confirmPasswordReset,
    refreshUser,
  };
});
