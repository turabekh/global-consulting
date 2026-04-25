import { api } from 'src/boot/axios';

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  phone: string;
  is_email_verified: boolean;
  date_joined: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface SignupPayload {
  email: string;
  password1: string;
  password2: string;
  first_name?: string;
  last_name?: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
}

export interface VerifyEmailPayload {
  key: string;
}

export interface PasswordResetPayload {
  email: string;
}

export interface PasswordResetConfirmPayload {
  uid: string;
  token: string;
  new_password1: string;
  new_password2: string;
}

export const authService = {
  async login(payload: LoginPayload): Promise<LoginResponse> {
    const { data } = await api.post<LoginResponse>('/auth/login/', payload);
    return data;
  },

  async signup(payload: SignupPayload): Promise<{ detail: string }> {
    const { data } = await api.post<{ detail: string }>('/auth/registration/', payload);
    return data;
  },

  async logout(): Promise<{ detail: string }> {
    const { data } = await api.post<{ detail: string }>('/auth/logout/');
    return data;
  },

  async fetchUser(): Promise<User> {
    const { data } = await api.get<User>('/auth/user/');
    return data;
  },

  async verifyEmail(payload: VerifyEmailPayload): Promise<{ detail: string }> {
    const { data } = await api.post<{ detail: string }>(
      '/auth/registration/verify-email/',
      payload,
    );
    return data;
  },

  async requestPasswordReset(payload: PasswordResetPayload): Promise<{ detail: string }> {
    const { data } = await api.post<{ detail: string }>('/auth/password/reset/', payload);
    return data;
  },

  async confirmPasswordReset(payload: PasswordResetConfirmPayload): Promise<{ detail: string }> {
    const { data } = await api.post<{ detail: string }>('/auth/password/reset/confirm/', payload);
    return data;
  },

  async refreshToken(): Promise<{ access: string }> {
    const { data } = await api.post<{ access: string }>('/auth/token/refresh/');
    return data;
  },
};
