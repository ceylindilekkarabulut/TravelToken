const BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function get<T>(path: string): Promise<T> {
  const r = await fetch(`${BASE}${path}`);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const r = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export const api = {
  createGoal: (body: Record<string, unknown>) => post<{ goal_id: string }>("/api/goals/create", body),
  getGoal: (id: string) => get<import("@/types/api").GoalResponse>(`/api/goals/${id}`),
  listGoals: (wallet?: string) =>
    get<import("@/types/api").GoalResponse[]>(wallet ? `/api/goals/list/by-wallet?user_wallet=${wallet}` : "/api/goals/list/by-wallet"),
  createSponsorship: (body: Record<string, unknown>) => post("/api/sponsorships/create", body),
  getSponsorships: (goalId: string) =>
    get<import("@/types/api").SponsorshipResponse[]>(`/api/sponsorships/${goalId}`),
  getPriceHistory: (goalId: string) =>
    get<import("@/types/api").PriceHistoryEntry[]>(`/api/goals/${goalId}/price-history`),
  searchRoutes: (query: string) =>
    get<import("@/types/api").RouteResponse[]>(`/api/routes/search?query=${encodeURIComponent(query)}`),
  copyRoute: (id: string) => post(`/api/routes/${id}/copy`, {}),
};
