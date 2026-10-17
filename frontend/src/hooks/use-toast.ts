'use client'

import { useEffect, useState } from 'react'

export type ToastVariant = 'default' | 'destructive'

export interface ToastOptions {
  title?: string
  description?: string
  variant?: ToastVariant
}

export interface ToastItem extends ToastOptions {
  id: number
}

const TOAST_LIFETIME_MS = 4000

let nextId = 0
let toasts: ToastItem[] = []
const listeners = new Set<(items: ToastItem[]) => void>()

function emit() {
  for (const listener of listeners) listener(toasts)
}

export function toast(options: ToastOptions): { id: number; dismiss: () => void } {
  const id = ++nextId
  toasts = [...toasts, { id, variant: 'default', ...options }]
  emit()
  const dismiss = () => {
    toasts = toasts.filter((item) => item.id !== id)
    emit()
  }
  setTimeout(dismiss, TOAST_LIFETIME_MS)
  return { id, dismiss }
}

export function useToast() {
  const [items, setItems] = useState<ToastItem[]>(toasts)

  useEffect(() => {
    listeners.add(setItems)
    return () => {
      listeners.delete(setItems)
    }
  }, [])

  return {
    toasts: items,
    toast,
    dismiss: (id: number) => {
      toasts = toasts.filter((item) => item.id !== id)
      emit()
    },
  }
}
