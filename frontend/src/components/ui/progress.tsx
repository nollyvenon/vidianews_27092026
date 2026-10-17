import { forwardRef, type HTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

export interface ProgressProps extends HTMLAttributes<HTMLDivElement> {
  value?: number | null
  max?: number
}

export const Progress = forwardRef<HTMLDivElement, ProgressProps>(({ className, value, max = 100, ...props }, ref) => {
  const percent = Math.min(100, Math.max(0, ((value ?? 0) / max) * 100))
  return (
    <div
      ref={ref}
      role="progressbar"
      aria-valuemin={0}
      aria-valuemax={max}
      aria-valuenow={value ?? 0}
      className={cn('relative w-full overflow-hidden rounded-full bg-gray-200', className)}
      {...props}
    >
      <div className="h-full bg-blue-600 transition-all" style={{ width: `${percent}%` }} />
    </div>
  )
})
Progress.displayName = 'Progress'
