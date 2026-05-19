"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

interface Props {
  goalId: string;
  compact?: boolean;
}

export function GoalProgress({ goalId, compact }: Props) {
  const { data } = useQuery({
    queryKey: ["sponsorships", goalId],
    queryFn: () => api.getSponsorships(goalId),
    staleTime: 30_000,
  });

  const totalSol = data?.reduce((sum, s) => sum + s.amount_sol, 0) ?? 0;
  const targetSol = 10;
  const pct = Math.min(100, (totalSol / targetSol) * 100);

  if (compact) {
    return (
      <div>
        <div className="h-1.5 bg-surface-border rounded-full overflow-hidden">
          <div className="h-full bg-brand-light rounded-full transition-all" style={{ width: `${pct}%` }} />
        </div>
        <p className="text-xs text-slate-500 mt-1">{totalSol.toFixed(2)} / {targetSol} SOL</p>
      </div>
    );
  }

  return (
    <div className="bg-surface-card border border-surface-border rounded-xl p-4">
      <div className="flex justify-between text-sm mb-2">
        <span className="text-slate-400">Sponsorship Progress</span>
        <span className="font-semibold">{totalSol.toFixed(2)} / {targetSol} SOL</span>
      </div>
      <div className="h-3 bg-surface-border rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-brand to-brand-light rounded-full transition-all"
          style={{ width: `${pct}%` }}
        />
      </div>
      <p className="text-xs text-slate-500 mt-2">{data?.length ?? 0} sponsors</p>
    </div>
  );
}
