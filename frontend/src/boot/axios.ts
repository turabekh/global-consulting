import { defineBoot } from '#q-app/wrappers';
import axios, { type AxiosInstance } from 'axios';
import { i18n } from 'src/boot/i18n';

declare module 'vue' {
  interface ComponentCustomProperties {
    $api: AxiosInstance;
  }
}

const api = axios.create({
  baseURL: process.env.API_URL || 'http://localhost:8000/api',
  withCredentials: true,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
});

api.interceptors.request.use((config) => {
  config.headers['Accept-Language'] = i18n.global.locale.value;
  return config;
});

export default defineBoot(({ app }) => {
  app.config.globalProperties.$api = api;
});

export { api };
