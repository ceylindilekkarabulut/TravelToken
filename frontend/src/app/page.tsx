"use client";

import { useGoalsList } from "@/hooks/useGoalsList";
import { GoalCard } from "@/components/goals/GoalCard";
import { LoadingSpinner } from "@/components/shared/LoadingSpinner";
import Link from "next/link";

export default function HomePage() {
  const { data: goals, isLoading } = useGoalsList();

  return (
    <div className="container mx-auto px-4 py-12">
      <section className="text-center mb-16">
        <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-brand-light to-purple-300 bg-clip-text text-transparent">
          Throne Travel
        </h1>
        <p className="text-xl text-slate-400 mb-8">
          AI agents plan your dream trip. Community sponsors make it real.
        </p>
        <Link
          href="/create"
          className="bg-brand text-white px-8 py-3 rounded-xl font-semibold hover:bg-brand-dark transition-colors"
        >
          Create Your Goal
        </Link>
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-6">Trending Goals</h2>
        {isLoading ? (
          <LoadingSpinner />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {goals?.map((goal) => (
              <GoalCard key={goal.id} goal={goal} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
