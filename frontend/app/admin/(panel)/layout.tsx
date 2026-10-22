import { ReactNode } from "react";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { INTERNAL_API } from "../../server";
import { AdminProvider, AdminUser } from "../lib";
import Shell from "./Shell";

export const dynamic = "force-dynamic";

/** Every admin page is rendered only for a valid session; anything else goes to the sign-in page. */
export default async function PanelLayout({ children }: { children: ReactNode }) {
  const jar = await cookies();
  const session = jar.get("admin_session")?.value;
  if (!session) redirect("/admin/login");
  let me: { user: AdminUser; csrf_token: string } | null = null;
  try {
    const res = await fetch(`${INTERNAL_API}/api/v1/admin/auth/me`, {
      headers: { cookie: `admin_session=${session}` },
      cache: "no-store",
    });
    if (res.ok) me = await res.json();
  } catch {
    /* API unreachable: treated as signed out */
  }
  if (!me) redirect("/admin/login");
  return (
    <AdminProvider user={me.user} csrf={me.csrf_token}>
      <Shell user={me.user}>{children}</Shell>
    </AdminProvider>
  );
}
