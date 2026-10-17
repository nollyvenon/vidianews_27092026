import { type HTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

export type BadgeVariant = 'default' | 'secondary' | 'destructive' | 'outline'

const VARIANTS: Record<BadgeVariant, string> = {
  default: 'border-transparent bg-blue-600 text-white',
  secondary: 'border-transparent bg-gray-200 text-gray-900',
  destructive: 'border-transparent bg-red-600 text-white',
  outline: 'border-gray-300 text-gray-900',
}

export interface BadgeProps extends HTMLAttributes<HTMLDivElement> {
  variant?: BadgeVariant
}

export function Badge({ className, variant = 'default', ...props }: BadgeProps) {
  return (
    <div
      className={cn(
        'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold',
        VARIANTS[variant],
        className
      )}
      {...props}
    />
  )
}
