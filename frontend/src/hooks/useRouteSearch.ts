import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useRouteSearch(query: string) {
  return useQuery({
    queryKey: ["routes", query],
    queryFn: () => api.searchRoutes(query),
    staleTime: 120_000,
  });
}
