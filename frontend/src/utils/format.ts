export function formatDate(value: string | null | undefined, locale: string): string {
  if (!value) return '';
  try {
    const date = new Date(value);
    return new Intl.DateTimeFormat(locale === 'uz' ? 'uz-UZ' : 'en-GB', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    }).format(date);
  } catch {
    return '';
  }
}
