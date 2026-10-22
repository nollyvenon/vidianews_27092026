import * as React from 'react';
import { cn } from './utils';

export const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn('flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm disabled:opacity-50', className)}
      {...props}
    />
  )
);
Input.displayName = 'Input';
