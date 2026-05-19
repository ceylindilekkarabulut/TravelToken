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

      <section className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-4 mb-16">
        {[
          {
            title: "City Explorer",
            src: "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80",
          },
          {
            title: "Beach Escape",
            src: "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80",
          },
          {
            title: "Mountain Adventure",
            src: "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=900&q=80",
          },
          {
            title: "Culture Route",
            src: "https://images.unsplash.com/photo-1491553895911-0055eca6402d?auto=format&fit=crop&w=900&q=80",
          },
        ].map((item) => (
          <div key={item.title} className="group overflow-hidden rounded-3xl border border-slate-800 bg-slate-950 shadow-xl">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={item.src}
              alt={item.title}
              className="h-48 w-full object-cover transition-transform duration-500 group-hover:scale-105"
            />
            <div className="p-4">
              <p className="font-semibold text-white">{item.title}</p>
            </div>
          </div>
        ))}
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
