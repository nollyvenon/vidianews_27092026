'use client';

import * as React from 'react';
import { cn } from './utils';

const TabsContext = React.createContext<{ value?: string; setValue: (v: string) => void }>({
  setValue: () => {},
});

export interface TabsProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'defaultValue'> {
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
}

export function Tabs({ value, defaultValue, onValueChange, ...props }: TabsProps) {
  const [inner, setInner] = React.useState(defaultValue);
  const current = value ?? inner;
  const setValue = (v: string) => {
    setInner(v);
    onValueChange?.(v);
  };
  return (
    <TabsContext.Provider value={{ value: current, setValue }}>
      <div {...props} />
    </TabsContext.Provider>
  );
}

export const TabsList = ({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn('inline-flex flex-wrap items-center rounded-md bg-gray-100 p-1', className)} {...props} />
);

export function TabsTrigger({
  value,
  className,
  ...props
}: { value: string } & React.ButtonHTMLAttributes<HTMLButtonElement>) {
  const ctx = React.useContext(TabsContext);
  const active = ctx.value === value;
  return (
    <button
      type="button"
      className={cn(
        'rounded px-3 py-1.5 text-sm font-medium',
        active ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-600',
        className
      )}
      onClick={() => ctx.setValue(value)}
      {...props}
    />
  );
}

export function TabsContent({
  value,
  className,
  ...props
}: { value: string } & React.HTMLAttributes<HTMLDivElement>) {
  const ctx = React.useContext(TabsContext);
  if (ctx.value !== value) return null;
  return <div className={cn('mt-2', className)} {...props} />;
}
