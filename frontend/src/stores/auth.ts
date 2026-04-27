import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { setLocale } from 'src/boot/i18n';
import {
  authService,
  type LoginPayload,
  type PasswordResetConfirmPayload,
  type PasswordResetPayload,
  type SignupPayload,
  type User,
  type VerifyEmailPayload,
} from 'src/services/auth';
import { profileService, type ProfileUpdatePayload } from 'src/services/profile';
import { messagingSocket } from 'src/services/messaging-ws';
import { useMessagingStore } from 'src/stores/messaging';

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
      applyUserLocale();
      messagingSocket.connect();
      const messaging = useMessagingStore();
      messaging.startListening();
      void messaging.load();
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
      applyUserLocale();
      messagingSocket.connect();
      const messaging = useMessagingStore();
      messaging.startListening();
      void messaging.load();
    } finally {
      isLoading.value = false;
    }
  }

  async function loginWithGoogle(): Promise<void> {
    const { getOAuthAccessToken } = await import('src/services/oauth');
    const token = await getOAuthAccessToken('google');
    isLoading.value = true;
    try {
      const response = await authService.googleLogin(token);
      user.value = response.user;
      applyUserLocale();
      messagingSocket.connect();
      const messaging = useMessagingStore();
      messaging.startListening();
      void messaging.load();
    } finally {
      isLoading.value = false;
    }
  }

  async function loginWithFacebook(): Promise<void> {
    const { getOAuthAccessToken } = await import('src/services/oauth');
    const token = await getOAuthAccessToken('facebook');
    isLoading.value = true;
    try {
      const response = await authService.facebookLogin(token);
      user.value = response.user;
      applyUserLocale();
      messagingSocket.connect();
      const messaging = useMessagingStore();
      messaging.startListening();
      void messaging.load();
    } finally {
      isLoading.value = false;
    }
  }

  function applyUserLocale() {
    const lang = user.value?.profile?.language;
    if (lang === 'uz' || lang === 'en') {
      setLocale(lang);
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
      messagingSocket.disconnect();
      const messaging = useMessagingStore();
      messaging.reset();
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

  async function updateProfile(payload: ProfileUpdatePayload): Promise<void> {
    isLoading.value = true;
    try {
      user.value = await profileService.updateMe(payload);
    } finally {
      isLoading.value = false;
    }
  }

  async function uploadAvatar(file: File): Promise<void> {
    isLoading.value = true;
    try {
      user.value = await profileService.uploadAvatar(file);
    } finally {
      isLoading.value = false;
    }
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
    updateProfile,
    uploadAvatar,
    loginWithGoogle,
    loginWithFacebook,
  };
});
