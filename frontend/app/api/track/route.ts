import { NextRequest } from "next/server";

export const dynamic = "force-dynamic";
const API = process.env["INTERNAL_API_URL"] || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8100";

/** Relays the page-view beacon, passing on the visitor's network details the API needs (and then discards). */
export async function POST(req: NextRequest) {
  const fwd: Record<string, string> = { "content-type": "application/json" };
  for (const k of ["user-agent", "x-forwarded-for", "x-real-ip", "accept-language", "dnt", "sec-gpc"]) {
    const v = req.headers.get(k);
    if (v) fwd[k] = v;
  }
  try {
    const body = (await req.text()).slice(0, 2000);
    await fetch(`${API}/api/v1/site/track`, { method: "POST", headers: fwd, body, cache: "no-store" });
  } catch {
    /* analytics must never break a page */
  }
  return new Response(null, { status: 204 });
}
