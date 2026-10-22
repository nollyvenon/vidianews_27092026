import { NextRequest } from "next/server";

export const dynamic = "force-dynamic";
const API = process.env["INTERNAL_API_URL"] || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Same-origin proxy to the admin API, so the HttpOnly session cookie belongs to the
 * website itself and the browser never talks to the API host directly.
 */
async function proxy(req: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  const { path } = await params;
  const url = `${API}/api/v1/admin/${path.map(encodeURIComponent).join("/")}${req.nextUrl.search}`;
  const headers = new Headers();
  for (const k of ["content-type", "cookie", "x-csrf-token", "origin", "user-agent", "x-forwarded-for", "x-real-ip", "x-forwarded-proto"]) {
    const v = req.headers.get(k);
    if (v) headers.set(k, v);
  }
  const hasBody = !["GET", "HEAD"].includes(req.method);
  let upstream: Response;
  try {
    upstream = await fetch(url, {
      method: req.method,
      headers,
      body: hasBody ? await req.arrayBuffer() : undefined,
      redirect: "manual",
      cache: "no-store",
    });
  } catch {
    return Response.json({ detail: "The API is unreachable" }, { status: 502 });
  }
  const out = new Headers();
  const type = upstream.headers.get("content-type");
  if (type) out.set("content-type", type);
  out.set("cache-control", "no-store");
  for (const c of upstream.headers.getSetCookie()) out.append("set-cookie", c);
  return new Response(upstream.status === 204 ? null : await upstream.arrayBuffer(), { status: upstream.status, headers: out });
}

export { proxy as GET, proxy as POST, proxy as PUT, proxy as PATCH, proxy as DELETE };
