"use client";

import { useState } from "react";
import Link from "next/link";
import { MockAgentStreamPanel } from "@/components/agents/MockAgentStreamPanel";
import { AgentStreamPanel } from "@/components/agents/AgentStreamPanel";
import { RouteSearchBar } from "@/components/routes/RouteSearchBar";
import { RouteResultCard } from "@/components/routes/RouteResultCard";
import { SponsorModal } from "@/components/goals/SponsorModal";
import { Button } from "@/components/ui/Button";

const MOCK_ROUTES = [
  { id: "r1", origin: "Istanbul", destination: "Paris", description_md: "Cheap flights via ATH", copy_count: 12 },
  { id: "r2", origin: "Berlin", destination: "Barcelona", description_md: "Sun + beach combo", copy_count: 5 },
];

export default function DevPage() {
  const [useMockStream, setUseMockStream] = useState(true);
  const [showStream, setShowStream] = useState(false);
  const [query, setQuery] = useState("");
  const [openSponsor, setOpenSponsor] = useState(false);
  const [origin, setOrigin] = useState("Istanbul");
  const [destination, setDestination] = useState("Paris");
  const [budget, setBudget] = useState<number | null>(350);
  const [travelDate, setTravelDate] = useState<string | null>(null);
  const [returnDate, setReturnDate] = useState<string | null>(null);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Dev / Test Dashboard</h1>

      <section className="mb-8">
        <h2 className="font-semibold mb-3">Agent Stream</h2>
        <div className="flex items-center gap-3 mb-4">
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={useMockStream} onChange={(e) => setUseMockStream(e.target.checked)} />
            <span className="text-sm text-slate-400">Use Mock Stream</span>
          </label>
          <Button onClick={() => setShowStream((s) => !s)} variant="primary">{showStream ? "Hide" : "Show"} Stream</Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
          <input value={origin} onChange={(e) => setOrigin(e.target.value)} placeholder="Origin" className="bg-surface-card border border-surface-border px-3 py-2 rounded" />
          <input value={destination} onChange={(e) => setDestination(e.target.value)} placeholder="Destination" className="bg-surface-card border border-surface-border px-3 py-2 rounded" />
          <input value={budget ?? ""} onChange={(e) => setBudget(e.target.value ? Number(e.target.value) : null)} placeholder="Budget USD" type="number" className="bg-surface-card border border-surface-border px-3 py-2 rounded" />
        </div>

        <div className="flex gap-3 mb-4">
          <input type="date" onChange={(e) => setTravelDate(e.target.value)} className="bg-surface-card border border-surface-border px-3 py-2 rounded" />
          <input type="date" onChange={(e) => setReturnDate(e.target.value)} className="bg-surface-card border border-surface-border px-3 py-2 rounded" />
        </div>

        {showStream && (useMockStream ? <MockAgentStreamPanel origin={origin} destination={destination} budgetUsd={budget} travelDate={travelDate} returnDate={returnDate} /> : <AgentStreamPanel goalId="dev-goal-123" />)}
      </section>

      <section className="mb-8">
        <h2 className="font-semibold mb-3">Route Search</h2>
        <RouteSearchBar value={query} onChange={setQuery} />
        <div className="mt-4 space-y-3">
          {MOCK_ROUTES.filter(r => `${r.origin} ${r.destination}`.toLowerCase().includes(query.toLowerCase())).map(r => (
            <RouteResultCard key={r.id} route={r as any} />
          ))}
        </div>
      </section>

      <section className="mb-8">
        <h2 className="font-semibold mb-3">Sponsor Modal</h2>
        <Button onClick={() => setOpenSponsor(true)}>Open Sponsor Modal</Button>
        <SponsorModal open={openSponsor} onClose={() => setOpenSponsor(false)} goalId="dev-goal-123" />
      </section>

      <section>
        <h2 className="font-semibold mb-3">Utilities</h2>
        <div className="flex gap-3">
          <Link href="/">Return Home</Link>
          <Link href="/create">Create Goal</Link>
        </div>
      </section>
    </div>
  );
}
