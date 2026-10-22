"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Ad {
  advert_id: string;
  image_src: string;
  alt_text: string;
  click_url: string;
}

export type Placement = "home_top" | "home_sidebar" | "category_top" | "article_top" | "article_inline" | "article_bottom";

/** Shows one live advert for the slot, or nothing at all when there is none. */
export default function AdSlot({ placement, className = "" }: { placement: Placement; className?: string }) {
  const [ad, setAd] = useState<Ad | null>(null);

  useEffect(() => {
    let cancelled = false;
    fetch(`${API_URL}/api/v1/site/ads?placement=${placement}`, { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => !cancelled && setAd(d?.ad ?? null))
      .catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, [placement]);

  if (!ad) return null;
  return (
    <aside aria-label="Advertisement" data-advert-id={ad.advert_id} className={`text-center ${className}`}>
      <p className="mb-1 text-[10px] font-medium uppercase tracking-widest text-gray-400">Advertisement</p>
      <a href={ad.click_url} target="_blank" rel="sponsored noopener noreferrer" className="inline-block max-w-full">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={ad.image_src} alt={ad.alt_text} className="mx-auto max-h-60 w-auto max-w-full rounded-lg border border-gray-200" />
      </a>
    </aside>
  );
}
