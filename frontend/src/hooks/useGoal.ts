import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useGoal(id: string) {
  return useQuery({
    queryKey: ["goal", id],
    queryFn: () => api.getGoal(id),
    enabled: !!id,
    staleTime: 30_000,
  });
}
