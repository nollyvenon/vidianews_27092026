/** URL-safe slug of a headline, used in article addresses: /news/123-the-headline. */
export function slugify(title: string): string {
  return title
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80)
    .replace(/-+$/, "");
}

export const articlePath = (a: { id: number; title: string }) => {
  const slug = slugify(a.title);
  return slug ? `/news/${a.id}-${slug}` : `/news/${a.id}`;
};
