"use client";

import { ReactNode, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { AdminUser, useAdmin } from "../lib";

const NAV = [
  { href: "/admin", label: "Overview", icon: "▦" },
  { href: "/admin/analytics", label: "Analytics", icon: "▤" },
  { href: "/admin/content", label: "Content", icon: "✎" },
  { href: "/admin/news-fetch", label: "News fetching", icon: "⟳" },
  { href: "/admin/adverts", label: "Adverts", icon: "◈" },
  { href: "/admin/settings", label: "Settings & SEO", icon: "⚙" },
];

export default function Shell({ user, children }: { user: AdminUser; children: ReactNode }) {
  const path = usePathname();
  const { call } = useAdmin();
  const [open, setOpen] = useState(false);

  async function signOut() {
    await call("POST", "/auth/logout").catch(() => undefined);
    window.location.href = "/admin/login";
  }
  const active = (href: string) => (href === "/admin" ? path === "/admin" : path.startsWith(href));

  const nav = (
    <nav aria-label="Admin" className="flex flex-col gap-1 p-3">
      {NAV.map((n) => (
        <Link
          key={n.href}
          href={n.href}
          onClick={() => setOpen(false)}
          aria-current={active(n.href) ? "page" : undefined}
          className={`flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium ${
            active(n.href) ? "bg-blue-600 text-white" : "text-slate-300 hover:bg-slate-800 hover:text-white"
          }`}
        >
          <span aria-hidden className="w-4 text-center">
            {n.icon}
          </span>
          {n.label}
        </Link>
      ))}
    </nav>
  );

  return (
    <div className="min-h-screen bg-gray-50 lg:flex">
      <aside className="hidden w-60 flex-none bg-slate-900 lg:block">
        <div className="px-5 py-4 text-lg font-bold text-white">Admin</div>
        {nav}
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="sticky top-0 z-30 flex items-center gap-3 border-b border-gray-200 bg-white px-4 py-2.5">
          <button className="rounded p-1.5 text-gray-700 hover:bg-gray-100 lg:hidden" aria-label="Menu" onClick={() => setOpen(!open)}>
            ☰
          </button>
          <Link href="/" target="_blank" className="text-sm text-blue-700 hover:underline">
            View site ↗
          </Link>
          <div className="ml-auto flex items-center gap-3 text-sm">
            <span className="hidden text-gray-600 sm:inline">
              {user.email} <span className="rounded bg-gray-100 px-1.5 py-0.5 text-xs">{user.role}</span>
            </span>
            <button onClick={signOut} className="rounded-lg border border-gray-300 px-3 py-1.5 font-medium text-gray-800 hover:bg-gray-50">
              Sign out
            </button>
          </div>
        </header>
        {open && <div className="bg-slate-900 lg:hidden">{nav}</div>}
        <main className="mx-auto w-full max-w-7xl flex-1 p-4 sm:p-6">{children}</main>
      </div>
    </div>
  );
}
