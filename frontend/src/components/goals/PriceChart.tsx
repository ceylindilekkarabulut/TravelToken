"use client";

import { useQuery } from "@tanstack/react-query";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceDot } from "recharts";
import { api } from "@/lib/api";

interface Props {
  goalId: string;
}

export function PriceChart({ goalId }: Props) {
  const { data } = useQuery({
    queryKey: ["price-history", goalId],
    queryFn: () => api.getPriceHistory(goalId),
    staleTime: 60_000,
  });

  if (!data?.length) return <p className="text-slate-400">No price data yet.</p>;

  const chartData = data.map((d, i) => ({
    index: i,
    total: (d.flight_price_usd ?? 0) + (d.hotel_price_usd ?? 0),
    buy: d.is_buy_signal,
    date: new Date(d.recorded_at).toLocaleDateString(),
  }));

  return (
    <div className="bg-surface-card border border-surface-border rounded-xl p-4">
      <h3 className="font-semibold mb-4">Price History (Flight + Hotel)</h3>
      <ResponsiveContainer width="100%" height={240}>
        <LineChart data={chartData}>
          <XAxis dataKey="date" tick={{ fontSize: 11, fill: "#94A3B8" }} />
          <YAxis tick={{ fontSize: 11, fill: "#94A3B8" }} />
          <Tooltip contentStyle={{ background: "#1A1A2E", border: "1px solid #2D2D4E" }} />
          <Line type="monotone" dataKey="total" stroke="#A78BFA" strokeWidth={2} dot={false} />
          {chartData.filter((d) => d.buy).map((d) => (
            <ReferenceDot key={d.index} x={d.date} y={d.total} r={6} fill="#22C55E" />
          ))}
        </LineChart>
      </ResponsiveContainer>
      <p className="text-xs text-slate-500 mt-2">Green dots = buy signal</p>
    </div>
  );
}
