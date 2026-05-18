import { create } from "zustand";
import type { GoalResponse } from "@/types/api";

interface GoalStore {
  goals: GoalResponse[];
  setGoals: (goals: GoalResponse[]) => void;
  addGoal: (goal: GoalResponse) => void;
}

export const useGoalStore = create<GoalStore>((set) => ({
  goals: [],
  setGoals: (goals) => set({ goals }),
  addGoal: (goal) => set((s) => ({ goals: [goal, ...s.goals] })),
}));
