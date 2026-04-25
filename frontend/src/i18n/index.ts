import en from './en';
import uz from './uz';

export default {
  en,
  uz,
};

export const SUPPORTED_LOCALES = ['en', 'uz'] as const;
export type SupportedLocale = (typeof SUPPORTED_LOCALES)[number];
export const DEFAULT_LOCALE: SupportedLocale = 'en';

export function isSupportedLocale(value: string): value is SupportedLocale {
  return (SUPPORTED_LOCALES as readonly string[]).includes(value);
}
