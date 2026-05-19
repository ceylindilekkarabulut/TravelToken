"use client";

import { useEffect, useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useRouter } from "next/navigation";
import { AgentStatusBadge } from "./AgentStatusBadge";
import { BudgetSummary } from "@/components/goals/BudgetSummary";

interface AgentEvent {
  type: "agent_start" | "agent_complete" | "done" | "error";
  agent?: string;
  data?: Record<string, unknown>;
  goal_id?: string;
  report?: string;
}

interface Props {
  goalId: string;
  budgetUsd?: number | null;
}

export function AgentStreamPanel({ goalId, budgetUsd }: Props) {
  const router = useRouter();
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [done, setDone] = useState(false);
  const [report, setReport] = useState<string | null>(null);
  const [estimated, setEstimated] = useState<number | null>(null);
  const retryRef = useRef(0);
  const sseRef = useRef<EventSource | null>(null);

  useEffect(() => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/goals/${goalId}/stream`;

    function connect() {
      const sse = new EventSource(url);
      sseRef.current = sse;

      const handleEvent = (type: AgentEvent["type"]) => (e: MessageEvent) => {
        try {
          const data = JSON.parse(e.data);
          setEvents((prev) => [...prev, { type, ...data }]);
          // extract estimated cost if provided
          const est = (data as any).estimated_cost_usd ?? (data as any).amount_usd ?? null;
          if (typeof est === "number") setEstimated(est);
          if (data.report && typeof data.report === "string") {
            setReport((r) => (r ? r + "\n" + data.report : data.report));
          }
          if (type === "done") {
            setDone(true);
            sse.close();
            setTimeout(() => router.push(`/goals/${goalId}`), 2000);
          }
        } catch (err) {
          console.error("Failed to parse SSE data", err);
        }
      };

      sse.addEventListener("agent_start", handleEvent("agent_start"));
      sse.addEventListener("agent_complete", handleEvent("agent_complete"));
      sse.addEventListener("done", handleEvent("done"));
      sse.addEventListener("error", handleEvent("error"));

      sse.onopen = () => {
        retryRef.current = 0;
      };

      sse.onerror = () => {
        sse.close();
        const retry = retryRef.current;
        if (retry < 5) {
          const timeout = Math.min(30_000, 1000 * 2 ** retry);
          retryRef.current += 1;
          setTimeout(connect, timeout);
        } else {
          setEvents((prev) => [...prev, { type: "error", agent: "System", data: { message: "Unable to connect to agent stream." } }]);
        }
      };
    }

    connect();

    return () => {
      sseRef.current?.close();
    };
  }, [goalId, router]);

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <h1 className="text-2xl font-bold mb-8">AI Agents Planning Your Trip...</h1>
      <div className="space-y-3">
        <AnimatePresence>
          {events.map((ev, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-surface-card border border-surface-border rounded-xl p-4 flex items-center gap-3"
            >
              <AgentStatusBadge type={ev.type} />
              <div>
                <p className="font-medium capitalize">{ev.agent || "System"}</p>
                <p className="text-sm text-slate-400">
                  {ev.type === "agent_start" && "Working..."}
                  {ev.type === "agent_complete" && "Completed"}
                  {ev.type === "done" && "All done! Redirecting..."}
                </p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
      {report && (
        <div className="mt-6 bg-surface-card border border-surface-border rounded-xl p-4">
          <h2 className="font-semibold mb-2">AI Report</h2>
          <pre className="whitespace-pre-wrap text-sm text-slate-300">{report}</pre>
        </div>
      )}
      <BudgetSummary estimated={estimated} budget={budgetUsd ?? null} />
      {!events.length && (
        <div className="flex items-center gap-3 text-slate-400">
          <span className="animate-spin">⟳</span>
          <span>Connecting to AI agents...</span>
        </div>
      )}
    </div>
  );
}
