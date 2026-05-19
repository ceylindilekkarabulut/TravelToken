import Link from "next/link";
import { GoalProgress } from "./GoalProgress";
import type { GoalResponse } from "@/types/api";

interface Props {
  goal: GoalResponse;
}

export function GoalCard({ goal }: Props) {
  return (
    <Link href={`/goals/${goal.id}`}>
      <div className="bg-surface-card border border-surface-border rounded-2xl p-6 hover:border-brand transition-all cursor-pointer group">
        <div className="flex items-start justify-between mb-3">
          <h3 className="font-semibold text-lg group-hover:text-brand-light transition-colors">
            {goal.origin} → {goal.destination}
          </h3>
          <span className={`text-xs px-2 py-1 rounded-full font-medium ${
            goal.status === "completed" ? "bg-green-900 text-green-300" :
            goal.status === "processing" ? "bg-yellow-900 text-yellow-300" :
            "bg-slate-800 text-slate-300"
          }`}>
            {goal.status}
          </span>
        </div>
        <p className="text-slate-400 text-sm mb-4">{goal.travel_date} · ${goal.budget_usd}</p>
        <GoalProgress goalId={goal.id} compact />
      </div>
    </Link>
  );
}
