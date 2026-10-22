import Link from "next/link";
import { apiGet } from "./server";

export default async function SiteFooter({ name }: { name: string }) {
  const pages = (await apiGet<{ items: { slug: string; title: string }[] }>("/site/pages"))?.items ?? [];
  return (
    <footer className="mt-8 border-t border-gray-200 bg-white py-6 text-center text-sm text-gray-500">
      <nav aria-label="Site" className="mb-2 flex justify-center gap-4">
        {pages.map((p) => (
          <Link key={p.slug} href={`/p/${p.slug}`} className="hover:underline">
            {p.title}
          </Link>
        ))}
      </nav>
      © {new Date().getFullYear()} {name}
    </footer>
  );
}
