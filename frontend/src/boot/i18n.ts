import { defineBoot } from '#q-app/wrappers';
import { createI18n } from 'vue-i18n';
import messages, { DEFAULT_LOCALE, isSupportedLocale, type SupportedLocale } from 'src/i18n';

export type MessageLanguages = keyof typeof messages;
export type MessageSchema = (typeof messages)['en'];

const LOCALE_STORAGE_KEY = 'gc-locale';

function detectLocale(): SupportedLocale {
  if (typeof window === 'undefined') {
    return DEFAULT_LOCALE;
  }

  const stored = window.localStorage.getItem(LOCALE_STORAGE_KEY);
  if (stored && isSupportedLocale(stored)) {
    return stored;
  }

  const browser = window.navigator.language.split('-')[0];
  if (browser && isSupportedLocale(browser)) {
    return browser;
  }

  return DEFAULT_LOCALE;
}

export const i18n = createI18n({
  locale: detectLocale(),
  fallbackLocale: DEFAULT_LOCALE,
  legacy: false,
  messages,
});

export function setLocale(locale: SupportedLocale): void {
  i18n.global.locale.value = locale;
  if (typeof window !== 'undefined') {
    window.localStorage.setItem(LOCALE_STORAGE_KEY, locale);
    window.document.documentElement.lang = locale;
  }
}

/* eslint-disable @typescript-eslint/no-empty-object-type */
declare module 'vue-i18n' {
  export interface DefineLocaleMessage extends MessageSchema {}
  export interface DefineDateTimeFormat {}
  export interface DefineNumberFormat {}
}
/* eslint-enable @typescript-eslint/no-empty-object-type */

export default defineBoot(({ app }) => {
  app.use(i18n);
  if (typeof window !== 'undefined') {
    window.document.documentElement.lang = i18n.global.locale.value;
  }
});
