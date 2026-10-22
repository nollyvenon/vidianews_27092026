import * as React from 'react';
import { cn } from './utils';

export interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: number;
}

export function Progress({ className, value = 0, ...props }: ProgressProps) {
  const pct = Math.min(100, Math.max(0, value));
  return (
    <div className={cn('h-2 w-full overflow-hidden rounded-full bg-gray-200', className)} {...props}>
      <div className="h-full bg-blue-600 transition-all" style={{ width: `${pct}%` }} />
    </div>
  );
}
