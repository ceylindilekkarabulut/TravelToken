"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { AgentStatusBadge } from "./AgentStatusBadge";
import { BudgetSummary } from "@/components/goals/BudgetSummary";

interface Props {
  onDone?: () => void;
  origin?: string;
  destination?: string;
  budgetUsd?: number | null;
  travelDate?: string | null;
  returnDate?: string | null;
}

export function MockAgentStreamPanel({ onDone, origin = "Istanbul", destination = "Paris", budgetUsd = null, travelDate = null, returnDate = null }: Props) {
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    let mounted = true;
    // deterministic estimate based on origin+destination
    const seed = (origin + "->" + destination).split("").reduce((s, c) => s + c.charCodeAt(0), 0);
    const base = 100 + (seed % 400); // 100..499
    // apply budget influence: if budget provided, nudge estimate toward budget
    const ratio = budgetUsd ? Math.min(1.4, Math.max(0.6, budgetUsd / (base || 1))) : 1;
    const estimated = Math.max(50, Math.round(base * ratio * 10) / 10);
    const breakdown = `Base: $${base.toFixed(2)} · Budget ratio: ${ratio.toFixed(2)} → Estimated: $${estimated.toFixed(2)}`;

    const seq = [
      { type: "agent_start", agent: "RouteAgent", data: { detail: `Calculating routes ${origin} → ${destination}` } },
      { type: "agent_complete", agent: "RouteAgent", data: { detail: "Routes ready", travel_date: travelDate ?? "2026-08-01", return_date: returnDate ?? "2026-08-10" } },
      { type: "agent_start", agent: "DealHunter", data: { detail: "Scanning fares" } },
      { type: "agent_complete", agent: "DealHunter", data: { detail: "Deals found", estimated_cost_usd: estimated, breakdown }, report: `Found flight+hotel estimate: $${estimated}` },
      { type: "done", agent: "Orchestrator", report: `Final plan compiled. Estimated total: $${estimated}` },
    ];

    let i = 0;
    function tick() {
      if (!mounted) return;
      const ev = seq[i];
      setEvents((s) => [...s, ev]);
      i += 1;
      if (i < seq.length) setTimeout(tick, 1200 + Math.random() * 1000);
      else if (onDone) setTimeout(onDone, 1000);
    }

    setTimeout(tick, 600);
    return () => {
      mounted = false;
    };
  }, [onDone, origin, destination, budgetUsd, travelDate, returnDate]);

  const last = events.slice().reverse().find((e) => e.data?.estimated_cost_usd || e.report);
  const estimated = last?.data?.estimated_cost_usd ?? null;
  const breakdown = last?.data?.breakdown ?? null;

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <h1 className="text-2xl font-bold mb-8">(Mock) AI Agents Planning...</h1>
      <div className="space-y-3">
        <AnimatePresence>
          {events.map((ev, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="bg-surface-card border border-surface-border rounded-xl p-4 flex items-center gap-3"
            >
              <AgentStatusBadge type={ev.type} />
              <div>
                <p className="font-medium">{ev.agent}</p>
                <p className="text-sm text-slate-400">{ev.data?.detail ?? ev.report ?? "Working..."}</p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
      <BudgetSummary estimated={estimated} />
      {breakdown && (
        <p className="text-xs text-slate-500 mt-2">Estimate breakdown: {breakdown}</p>
      )}
    </div>
  );
}
