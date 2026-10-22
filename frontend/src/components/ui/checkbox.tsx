import * as React from 'react';
import { cn } from './utils';

export interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type' | 'onChange'> {
  onCheckedChange?: (checked: boolean) => void;
}

export const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className, onCheckedChange, ...props }, ref) => (
    <input
      ref={ref}
      type="checkbox"
      className={cn('h-4 w-4 rounded border-gray-300', className)}
      onChange={(e) => onCheckedChange?.(e.target.checked)}
      {...props}
    />
  )
);
Checkbox.displayName = 'Checkbox';
