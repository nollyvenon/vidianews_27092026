"use client";

import { useState } from "react";
import { fmtNum } from "./lib";

export interface Point {
  label: string;
  value: number;
}

const niceMax = (v: number) => {
  if (v <= 4) return 4;
  const mag = 10 ** Math.floor(Math.log10(v));
  return Math.ceil(v / mag) * mag;
};

/** Single-series column chart: one hue, thin columns, quiet grid, hover tooltip, and a table view. */
export function BarChart({ points, name, height = 220 }: { points: Point[]; name: string; height?: number }) {
  const [hover, setHover] = useState<number | null>(null);
  const [table, setTable] = useState(false);
  const W = 640;
  const pad = { l: 40, r: 8, t: 10, b: 24 };
  const max = niceMax(Math.max(0, ...points.map((p) => p.value)));
  const innerW = W - pad.l - pad.r;
  const innerH = height - pad.t - pad.b;
  const slot = points.length ? innerW / points.length : innerW;
  const barW = Math.min(22, Math.max(3, slot * 0.6));
  const y = (v: number) => pad.t + innerH - (v / max) * innerH;
  const every = Math.ceil(points.length / 8);
  const total = points.reduce((s, p) => s + p.value, 0);

  if (table) {
    return (
      <div>
        <button className="mb-2 text-xs text-blue-700 hover:underline" onClick={() => setTable(false)}>
          Show chart
        </button>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-xs text-gray-500">
              <th className="py-1 font-medium">Period</th>
              <th className="py-1 text-right font-medium">{name}</th>
            </tr>
          </thead>
          <tbody>
            {points.map((p) => (
              <tr key={p.label} className="border-t border-gray-100">
                <td className="py-1">{p.label}</td>
                <td className="py-1 text-right tabular-nums">{fmtNum(p.value)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  return (
    <div className="relative">
      <svg viewBox={`0 0 ${W} ${height}`} className="w-full" role="img" aria-label={`${name} by period, ${fmtNum(total)} in total`}>
        {[0, 0.5, 1].map((f) => (
          <g key={f}>
            <line x1={pad.l} x2={W - pad.r} y1={y(max * f)} y2={y(max * f)} stroke="#e5e7eb" strokeWidth={1} />
            <text x={pad.l - 6} y={y(max * f) + 4} textAnchor="end" fontSize={11} fill="#6b7280">
              {fmtNum(Math.round(max * f))}
            </text>
          </g>
        ))}
        {points.map((p, i) => {
          const cx = pad.l + slot * i + slot / 2;
          const h = Math.max(p.value > 0 ? 2 : 0, (p.value / max) * innerH);
          return (
            <g key={p.label} onMouseEnter={() => setHover(i)} onMouseLeave={() => setHover(null)} onFocus={() => setHover(i)} onBlur={() => setHover(null)} tabIndex={0}>
              <rect x={pad.l + slot * i} y={pad.t} width={slot} height={innerH} fill="transparent" />
              <rect x={cx - barW / 2} y={pad.t + innerH - h} width={barW} height={h} rx={3} fill={hover === i ? "#1d4ed8" : "#2563eb"} />
              {i % every === 0 && (
                <text x={cx} y={height - 6} textAnchor="middle" fontSize={11} fill="#6b7280">
                  {p.label}
                </text>
              )}
            </g>
          );
        })}
      </svg>
      {hover !== null && (
        <div
          className="pointer-events-none absolute top-0 -translate-x-1/2 rounded-md border border-gray-200 bg-white px-2.5 py-1.5 text-xs shadow-md"
          style={{ left: `${((pad.l + slot * hover + slot / 2) / W) * 100}%` }}
        >
          <div className="text-gray-500">{points[hover].label}</div>
          <div className="font-semibold text-gray-900">
            {fmtNum(points[hover].value)} {name.toLowerCase()}
          </div>
        </div>
      )}
      <button className="mt-1 text-xs text-blue-700 hover:underline" onClick={() => setTable(true)}>
        Show as table
      </button>
    </div>
  );
}

/** Ranked horizontal bars with the value written beside each: for pages, countries, sources. */
export function RankList({ rows, empty = "No data yet" }: { rows: { label: string; sub?: string; value: number }[]; empty?: string }) {
  if (rows.length === 0) return <p className="py-4 text-sm text-gray-500">{empty}</p>;
  const max = Math.max(...rows.map((r) => r.value), 1);
  return (
    <ul className="space-y-2.5">
      {rows.map((r) => (
        <li key={r.label}>
          <div className="flex items-baseline justify-between gap-3 text-sm">
            <span className="min-w-0 truncate text-gray-800" title={r.label}>
              {r.label}
            </span>
            <span className="flex-none font-medium tabular-nums text-gray-900">{fmtNum(r.value)}</span>
          </div>
          {r.sub && <div className="truncate text-xs text-gray-500">{r.sub}</div>}
          <div className="mt-1 h-1.5 rounded-full bg-gray-100">
            <div className="h-1.5 rounded-full bg-blue-600" style={{ width: `${Math.max(2, (r.value / max) * 100)}%` }} />
          </div>
        </li>
      ))}
    </ul>
  );
}
