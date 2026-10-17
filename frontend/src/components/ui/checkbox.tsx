import { forwardRef, type InputHTMLAttributes } from 'react'
import { cn } from '@/lib/utils'

export interface CheckboxProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'type' | 'onChange'> {
  onCheckedChange?: (checked: boolean) => void
}

export const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(({ className, onCheckedChange, ...props }, ref) => (
  <input
    ref={ref}
    type="checkbox"
    onChange={(e) => onCheckedChange?.(e.target.checked)}
    className={cn(
      'h-4 w-4 rounded border-gray-300 text-blue-600 focus-visible:ring-2 focus-visible:ring-blue-500 disabled:opacity-50',
      className
    )}
    {...props}
  />
))
Checkbox.displayName = 'Checkbox'
