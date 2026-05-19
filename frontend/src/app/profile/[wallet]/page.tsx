"use client";

import { useParams } from "next/navigation";
import { useGoalsList } from "@/hooks/useGoalsList";
import { GoalCard } from "@/components/goals/GoalCard";
import { LoadingSpinner } from "@/components/shared/LoadingSpinner";

export default function ProfilePage() {
  const { wallet } = useParams<{ wallet: string }>();
  const { data: goals, isLoading } = useGoalsList(wallet);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center gap-4 mb-8">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={`https://api.dicebear.com/9.x/identicon/svg?seed=${wallet}`}
          alt="avatar"
          className="w-16 h-16 rounded-full border-2 border-brand"
        />
        <div>
          <h1 className="text-2xl font-bold">Travel Profile</h1>
          <p className="text-slate-400 text-sm font-mono">{wallet.slice(0, 8)}...{wallet.slice(-8)}</p>
        </div>
      </div>

      <h2 className="text-xl font-semibold mb-4">Goals</h2>
      {isLoading ? (
        <LoadingSpinner />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {goals?.map((goal) => (
            <GoalCard key={goal.id} goal={goal} />
          ))}
        </div>
      )}
    </div>
  );
}
