"use client";

import { useEffect, useRef } from "react";
import { usePathname } from "next/navigation";

/** Sends one anonymous page view per navigation. No cookies, no identifiers. */
export default function Tracker() {
  const pathname = usePathname();
  const last = useRef<string | null>(null);
  const first = useRef(true);

  useEffect(() => {
    if (!pathname || pathname.startsWith("/admin") || last.current === pathname) return;
    last.current = pathname;
    if (navigator.doNotTrack === "1") return;
    // document.referrer only describes how the visit started, so it is sent once.
    const referrer = first.current ? document.referrer : "";
    first.current = false;
    fetch("/api/track", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ path: pathname, referrer }),
      keepalive: true,
    }).catch(() => undefined);
  }, [pathname]);

  return null;
}
