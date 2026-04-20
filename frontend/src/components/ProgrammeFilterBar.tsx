import { useMemo } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { ChevronLeft, ChevronRight, X } from "lucide-react";
import { useProgrammes } from "@/hooks/usePortfolio";
import type { Programme } from "@/lib/api";

export type CrossTabLink = {
  /** Route path, without the query string. */
  to: string;
  /** Shown to the user. */
  label: string;
};

type Props = {
  /** Route path of the page rendering this bar, used when navigating peers. */
  currentRoute: string;
  /** Cross-tab links surfaced when a programme filter is active. */
  crossLinks?: CrossTabLink[];
  /**
   * Optional override when the page drives selection via local state instead of
   * the `?programme=CODE` query param (e.g. CustomerIntelligence programme picker).
   */
  activeProgramme?: Programme | null;
  /**
   * Pure-local mode: if provided, prev/next + clear call this callback instead
   * of rewriting the URL. The filter chip is still shown.
   */
  onSelect?: (programme: Programme | null) => void;
};

export function ProgrammeFilterBar({
  currentRoute,
  crossLinks = [],
  activeProgramme,
  onSelect,
}: Props) {
  const programmes = useProgrammes();
  const [searchParams, setSearchParams] = useSearchParams();
  const codeFromUrl = searchParams.get("programme");

  const fromUrl = useMemo(
    () => programmes.data?.find((p) => p.code === codeFromUrl) ?? null,
    [programmes.data, codeFromUrl],
  );
  const effective = activeProgramme ?? fromUrl;

  if (!effective || (programmes.data?.length ?? 0) === 0) return null;

  const list = programmes.data ?? [];
  const idx = list.findIndex((p) => p.id === effective.id);
  const prev = idx > 0 ? list[idx - 1] : list[list.length - 1];
  const next = idx < list.length - 1 ? list[idx + 1] : list[0];

  function navigate(target: Programme | null) {
    if (onSelect) {
      onSelect(target);
      return;
    }
    const params = new URLSearchParams(searchParams);
    if (target) {
      params.set("programme", target.code);
    } else {
      params.delete("programme");
    }
    setSearchParams(params);
  }

  return (
    <div className="flex flex-wrap items-center gap-2 self-start text-xs">
      <div className="inline-flex items-center gap-1 rounded-full border border-navy/30 bg-navy/5 px-2 py-0.5 text-navy">
        <button
          type="button"
          onClick={() => navigate(prev)}
          aria-label={`Previous programme (${prev.code})`}
          className="rounded-full p-1 hover:bg-navy/10"
          disabled={list.length <= 1}
        >
          <ChevronLeft className="size-3" aria-hidden="true" />
        </button>
        <span className="px-1 font-medium">{effective.name}</span>
        <button
          type="button"
          onClick={() => navigate(next)}
          aria-label={`Next programme (${next.code})`}
          className="rounded-full p-1 hover:bg-navy/10"
          disabled={list.length <= 1}
        >
          <ChevronRight className="size-3" aria-hidden="true" />
        </button>
        <button
          type="button"
          onClick={() => navigate(null)}
          aria-label="Clear programme filter (drill up)"
          className="inline-flex items-center gap-0.5 rounded-full bg-navy/10 px-1.5 py-0.5 hover:bg-navy/20"
        >
          <X className="size-3" aria-hidden="true" /> clear
        </button>
      </div>

      {crossLinks.length > 0 ? (
        <div className="flex flex-wrap items-center gap-1 text-navy/70">
          <span className="pl-1 text-navy/50">Open in:</span>
          {crossLinks
            .filter((link) => link.to !== currentRoute)
            .map((link) => (
              <Link
                key={link.to}
                to={`${link.to}?programme=${effective.code}`}
                className="rounded-full border border-ice-100 bg-white px-2 py-0.5 transition hover:bg-ice-50"
              >
                {link.label}
              </Link>
            ))}
        </div>
      ) : null}
    </div>
  );
}

