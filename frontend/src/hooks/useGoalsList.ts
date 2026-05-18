import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useGoalsList(wallet?: string) {
  return useQuery({
    queryKey: ["goals", wallet],
    queryFn: () => api.listGoals(wallet),
    staleTime: 60_000,
  });
}
