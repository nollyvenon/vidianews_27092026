"use client";

import { useEffect, useState } from "react";
import { newsApi } from "../api";
import { FallbackImage } from "../components";

/** Counts the visit towards the trending score once the page is shown. */
export function ClickBeacon({ id }: { id: number }) {
  useEffect(() => {
    newsApi.click(id);
  }, [id]);
  return null;
}

export function ArticleImage(props: {
  title: string;
  category: string;
  image_url: string | null;
  image_source: string | null;
  image_credit: string | null;
  image_credit_url: string | null;
}) {
  const [failed, setFailed] = useState(false);
  if (!props.image_url || failed) {
    return <FallbackImage category={props.category} className="h-56 w-full rounded-xl sm:h-80" />;
  }
  return (
    <figure>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={props.image_url}
        alt={props.title}
        referrerPolicy="no-referrer"
        className="max-h-[32rem] w-full rounded-xl bg-slate-100 object-cover"
        onError={() => setFailed(true)}
      />
      <figcaption className="mt-1 text-xs text-gray-500">
        {props.image_source === "wikimedia" && <span className="mr-1 font-medium">Illustrative image.</span>}
        {props.image_credit_url ? (
          <a href={props.image_credit_url} target="_blank" rel="noopener noreferrer" className="underline hover:text-gray-700">
            {props.image_credit}
          </a>
        ) : (
          props.image_credit
        )}
      </figcaption>
    </figure>
  );
}
