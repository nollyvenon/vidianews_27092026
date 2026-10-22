import * as React from 'react';
import { cn } from './utils';

type DivProps = React.HTMLAttributes<HTMLDivElement>;

export const Card = ({ className, ...props }: DivProps) => (
  <div className={cn('rounded-lg border border-gray-200 bg-white shadow-sm', className)} {...props} />
);
export const CardHeader = ({ className, ...props }: DivProps) => (
  <div className={cn('flex flex-col space-y-1.5 p-6', className)} {...props} />
);
export const CardTitle = ({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
  <h3 className={cn('text-lg font-semibold leading-none', className)} {...props} />
);
export const CardDescription = ({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) => (
  <p className={cn('text-sm text-gray-500', className)} {...props} />
);
export const CardContent = ({ className, ...props }: DivProps) => (
  <div className={cn('p-6 pt-0', className)} {...props} />
);
export const CardFooter = ({ className, ...props }: DivProps) => (
  <div className={cn('flex items-center p-6 pt-0', className)} {...props} />
);
