'use client';

export interface ToastOptions {
  title?: string;
  description?: string;
  variant?: 'default' | 'destructive';
}

export function useToast() {
  const toast = ({ title, description, variant }: ToastOptions) => {
    const log = variant === 'destructive' ? console.error : console.log;
    log(`[toast] ${title ?? ''} ${description ?? ''}`.trim());
  };
  return { toast };
}
