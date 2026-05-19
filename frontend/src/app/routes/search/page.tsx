"use client";

export const dynamic = "force-dynamic";

import { useEffect, useState } from "react";
import { useRouteSearch } from "@/hooks/useRouteSearch";
import { RouteSearchBar } from "@/components/routes/RouteSearchBar";
import { RouteResultCard } from "@/components/routes/RouteResultCard";
import { LoadingSpinner } from "@/components/shared/LoadingSpinner";

export default function RouteSearchPage() {
  const [query, setQuery] = useState("");

  useEffect(() => {
    const q = typeof window !== "undefined" ? new URLSearchParams(window.location.search).get("q") ?? "" : "";
    setQuery(q);
  }, []);

  const { data: routes, isLoading } = useRouteSearch(query);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Discover Routes</h1>
      <RouteSearchBar value={query} onChange={setQuery} />
      <div className="mt-8">
        {isLoading ? (
          <LoadingSpinner />
        ) : routes?.length ? (
          <div className="space-y-4">
            {routes.map((route) => (
              <RouteResultCard key={route.id} route={route} />
            ))}
          </div>
        ) : (
          <div className="rounded-2xl border border-surface-border bg-surface-card p-8 text-center text-slate-400">
            No routes matched your search yet. Try a different city or keyword.
          </div>
        )}
      </div>
    </div>
  );
}
