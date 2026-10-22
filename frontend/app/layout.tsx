import type { Metadata } from "next";
import { ReactNode } from "react";
import "./globals.css";
import Tracker from "./Tracker";
import { SITE_URL, getSettings } from "./server";

export const dynamic = "force-dynamic";

export async function generateMetadata(): Promise<Metadata> {
  const s = await getSettings();
  return {
    metadataBase: new URL(SITE_URL),
    title: { default: `${s.site_name} — ${s.site_tagline}`, template: `%s | ${s.site_name}` },
    description: s.site_description,
    applicationName: s.site_name,
    alternates: { canonical: "/" },
    robots: { index: true, follow: true },
    openGraph: {
      type: "website",
      siteName: s.site_name,
      title: s.site_name,
      description: s.site_description,
      url: "/",
      images: s.default_og_image ? [s.default_og_image] : undefined,
    },
    twitter: {
      card: s.default_og_image ? "summary_large_image" : "summary",
      site: s.twitter_handle || undefined,
    },
  };
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
        <Tracker />
      </body>
    </html>
  );
}
