'use client'

import { useToast } from '@/hooks/use-toast'
import { cn } from '@/lib/utils'

export function Toaster() {
  const { toasts, dismiss } = useToast()

  if (toasts.length === 0) return null

  return (
    <div
      aria-live="polite"
      className="fixed bottom-4 right-4 z-50 flex w-80 flex-col gap-2"
    >
      {toasts.map((item) => (
        <div
          key={item.id}
          role="status"
          className={cn(
            'rounded-lg border p-4 shadow-lg',
            item.variant === 'destructive'
              ? 'border-red-200 bg-red-50 text-red-900'
              : 'border-gray-200 bg-white text-gray-900'
          )}
        >
          <div className="flex items-start justify-between gap-2">
            <div>
              {item.title && <p className="font-semibold">{item.title}</p>}
              {item.description && <p className="text-sm">{item.description}</p>}
            </div>
            <button
              type="button"
              onClick={() => dismiss(item.id)}
              aria-label="Dismiss notification"
              className="text-sm text-gray-500 hover:text-gray-900"
            >
              ×
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}
