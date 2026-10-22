"use client";

import { createContext, useCallback, useContext, useMemo, useState, ReactNode } from "react";

export interface AdminUser {
  id: number;
  email: string;
  name: string | null;
  role: "admin" | "editor";
}

interface Ctx {
  user: AdminUser;
  call: <T = unknown>(method: string, path: string, body?: unknown) => Promise<T>;
  upload: <T = unknown>(path: string, file: File) => Promise<T>;
}

const AdminContext = createContext<Ctx | null>(null);

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

function messageOf(body: unknown, fallback: string): string {
  const detail = (body as { detail?: unknown })?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail) && detail[0]?.msg) {
    const where = Array.isArray(detail[0].loc) ? detail[0].loc.filter((p: unknown) => p !== "body").join(".") : "";
    return `${where ? where + ": " : ""}${detail[0].msg}`;
  }
  return fallback;
}

export async function rawCall<T>(method: string, path: string, csrf: string | null, body?: unknown): Promise<T> {
  const res = await fetch(`/api/admin${path}`, {
    method,
    credentials: "same-origin",
    headers: { ...(body !== undefined ? { "content-type": "application/json" } : {}), ...(csrf ? { "x-csrf-token": csrf } : {}) },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  const data = res.status === 204 ? null : await res.json().catch(() => null);
  if (!res.ok) throw new ApiError(res.status, messageOf(data, `${res.status} ${res.statusText}`));
  return data as T;
}

export function AdminProvider({ user, csrf, children }: { user: AdminUser; csrf: string; children: ReactNode }) {
  const [token] = useState(csrf);
  const expired = useCallback((e: unknown) => {
    if (e instanceof ApiError && e.status === 401) window.location.href = "/admin/login";
    throw e;
  }, []);
  const value = useMemo<Ctx>(
    () => ({
      user,
      call: (method, path, body) => rawCall(method, path, token, body).catch(expired) as never,
      upload: async (path, file) => {
        const form = new FormData();
        form.append("file", file);
        const res = await fetch(`/api/admin${path}`, { method: "POST", body: form, headers: { "x-csrf-token": token } });
        const data = await res.json().catch(() => null);
        if (!res.ok) throw new ApiError(res.status, messageOf(data, "Upload failed"));
        return data;
      },
    }),
    [user, token, expired]
  );
  return <AdminContext.Provider value={value}>{children}</AdminContext.Provider>;
}

export function useAdmin(): Ctx {
  const ctx = useContext(AdminContext);
  if (!ctx) throw new Error("useAdmin outside AdminProvider");
  return ctx;
}

export const fmtNum = (n: number | null | undefined) => (n ?? 0).toLocaleString("en-GB");

export function fmtDate(iso: string | null | undefined, withTime = true): string {
  if (!iso) return "—";
  return new Date(iso).toLocaleString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
    ...(withTime ? { hour: "2-digit", minute: "2-digit" } : {}),
  });
}

export function relTime(iso: string | null | undefined): string {
  if (!iso) return "never";
  const s = Math.round((new Date(iso).getTime() - Date.now()) / 1000);
  const abs = Math.abs(s);
  const unit = abs < 90 ? [Math.round(abs), "s"] : abs < 5400 ? [Math.round(abs / 60), "min"] : abs < 129600 ? [Math.round(abs / 3600), "h"] : [Math.round(abs / 86400), "d"];
  return s >= 0 ? `in ${unit[0]} ${unit[1]}` : `${unit[0]} ${unit[1]} ago`;
}
