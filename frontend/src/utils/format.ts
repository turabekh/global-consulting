import type { ApplicationListItem } from 'src/services/applications';

export interface ApplicationStats {
  total: number;
  drafts: number;
  inProgress: number;
  completed: number;
}

export function computeApplicationStats(items: ApplicationListItem[]): ApplicationStats {
  let drafts = 0;
  let inProgress = 0;
  let completed = 0;

  for (const item of items) {
    if (item.status === 'draft') drafts += 1;
    else if (
      item.status === 'submitted' ||
      item.status === 'in_review' ||
      item.status === 'needs_info'
    ) {
      inProgress += 1;
    } else if (
      item.status === 'accepted' ||
      item.status === 'rejected' ||
      item.status === 'closed'
    ) {
      completed += 1;
    }
  }

  return { total: items.length, drafts, inProgress, completed };
}

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
