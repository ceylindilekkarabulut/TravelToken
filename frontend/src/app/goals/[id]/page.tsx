"use client";

import { useParams } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import { useGoal } from "@/hooks/useGoal";
import { GoalProgress } from "@/components/goals/GoalProgress";
import { FinalReportRenderer } from "@/components/goals/FinalReportRenderer";
import { SponsorModal } from "@/components/goals/SponsorModal";
import { PriceChart } from "@/components/goals/PriceChart";
import { LoadingSpinner } from "@/components/shared/LoadingSpinner";
import { api } from "@/lib/api";
import { useState } from "react";

export default function GoalDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: goal, isLoading } = useGoal(id);
  const { data: sponsors } = useQuery({
    queryKey: ["sponsorships", id],
    queryFn: () => api.getSponsorships(id),
    enabled: Boolean(id),
  });
  const [activeTab, setActiveTab] = useState<"plan" | "sponsors" | "price">("plan");
  const [sponsorOpen, setSponsorOpen] = useState(false);

  if (isLoading) return <LoadingSpinner />;
  if (!goal) return <div className="p-8 text-center text-slate-400">Goal not found</div>;

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="flex items-start justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold">{goal.origin} → {goal.destination}</h1>
          <p className="text-slate-400 mt-1">{goal.travel_date} · Budget ${goal.budget_usd}</p>
        </div>
        <button
          onClick={() => setSponsorOpen(true)}
          className="bg-brand text-white px-6 py-2 rounded-xl font-semibold hover:bg-brand-dark transition-colors"
        >
          Sponsor
        </button>
      </div>

      <GoalProgress goalId={id} />

      <div className="flex gap-4 mt-8 mb-6 border-b border-surface-border">
        {(["plan", "sponsors", "price"] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`pb-3 px-1 font-medium capitalize transition-colors ${
              activeTab === tab
                ? "text-brand-light border-b-2 border-brand-light"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {activeTab === "plan" && <FinalReportRenderer markdown={goal.final_report_md || ""} />}
      {activeTab === "sponsors" && (
        <div className="space-y-4">
          {sponsors?.length ? (
            sponsors.map((sponsor) => (
              <div key={sponsor.id} className="bg-surface-card border border-surface-border rounded-xl p-4">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="font-semibold">{sponsor.sponsor_wallet}</p>
                    <p className="text-slate-400 text-sm">{sponsor.tx_signature || "No tx recorded"}</p>
                  </div>
                  <span className="text-sm text-green-300">{sponsor.amount_sol.toFixed(2)} SOL</span>
                </div>
              </div>
            ))
          ) : (
            <div className="rounded-2xl border border-surface-border bg-surface-card p-8 text-center text-slate-400">
              Henüz sponsorluk yok. İlk sponsoru bekliyoruz.
            </div>
          )}
        </div>
      )}
      {activeTab === "price" && <PriceChart goalId={id} />}

      <SponsorModal open={sponsorOpen} onClose={() => setSponsorOpen(false)} goalId={id} />
    </div>
  );
}
