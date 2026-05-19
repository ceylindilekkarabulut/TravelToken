"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { api } from "@/lib/api";
import { AgentStreamPanel } from "@/components/agents/AgentStreamPanel";
import { useWalletStore } from "@/stores/walletStore";

const schema = z.object({
  destination: z.string().min(2),
  origin: z.string().min(2),
  travel_date: z.string().min(6),
  return_date: z.string().min(6),
  budget_usd: z.number().min(100),
  preferences: z.string().optional(),
});

type FormData = z.infer<typeof schema>;

export default function CreateGoalPage() {
  const router = useRouter();
  const { wallet } = useWalletStore();
  const [goalId, setGoalId] = useState<string | null>(null);
  const [submittedBudget, setSubmittedBudget] = useState<number | null>(null);

  const { register, handleSubmit, formState: { errors, isSubmitting }, reset } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  useEffect(() => {
    // read query params from window.location (client-only)
    if (typeof window === "undefined") return;
    const sp = new URLSearchParams(window.location.search);
    const originParam = sp.get("origin");
    const destinationParam = sp.get("destination");
    if (originParam || destinationParam) {
      reset({
        origin: originParam ?? "",
        destination: destinationParam ?? "",
        travel_date: "",
        return_date: "",
        budget_usd: 0 as any,
        preferences: "",
      });
    }
  }, [reset]);

  const onSubmit = async (data: FormData) => {
    const response = await api.createGoal({ ...data, user_wallet: wallet || "anonymous" });
    setSubmittedBudget(data.budget_usd ?? null);
    setGoalId(response.goal_id);
  };

  if (goalId) {
    return <AgentStreamPanel goalId={goalId} budgetUsd={submittedBudget} />;
  }

  return (
    <div className="container mx-auto px-4 py-12 max-w-lg">
      <h1 className="text-3xl font-bold mb-8">Create Travel Goal</h1>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Origin</label>
          <input
            {...register("origin")}
            placeholder="Istanbul"
            className="w-full bg-surface-card border border-surface-border rounded-lg px-4 py-2 focus:ring-2 focus:ring-brand outline-none"
          />
          {errors.origin && <p className="text-red-400 text-sm mt-1">{errors.origin.message}</p>}
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Destination</label>
          <input
            {...register("destination")}
            placeholder="Paris"
            className="w-full bg-surface-card border border-surface-border rounded-lg px-4 py-2 focus:ring-2 focus:ring-brand outline-none"
          />
          {errors.destination && <p className="text-red-400 text-sm mt-1">{errors.destination.message}</p>}
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Travel Date</label>
          <input
            {...register("travel_date")}
            type="date"
            className="w-full bg-surface-card border border-surface-border rounded-lg px-4 py-2 focus:ring-2 focus:ring-brand outline-none"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Return Date</label>
          <input
            {...register("return_date")}
            type="date"
            className="w-full bg-surface-card border border-surface-border rounded-lg px-4 py-2 focus:ring-2 focus:ring-brand outline-none"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Budget (USD)</label>
          <input
            {...register("budget_usd", { valueAsNumber: true })}
            type="number"
            placeholder="1500"
            className="w-full bg-surface-card border border-surface-border rounded-lg px-4 py-2 focus:ring-2 focus:ring-brand outline-none"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Preferences</label>
          <textarea
            {...register("preferences")}
            placeholder="Budget travel, vegetarian food, historical sites..."
            rows={3}
            className="w-full bg-surface-card border border-surface-border rounded-lg px-4 py-2 focus:ring-2 focus:ring-brand outline-none resize-none"
          />
        </div>
        <button
          type="submit"
          disabled={isSubmitting}
          className="w-full bg-brand text-white py-3 rounded-xl font-semibold hover:bg-brand-dark transition-colors disabled:opacity-50"
        >
          {isSubmitting ? "Planning..." : "Start AI Planning"}
        </button>
      </form>
    </div>
  );
}
