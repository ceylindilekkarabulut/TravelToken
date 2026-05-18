"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useRouter } from "next/navigation";
import { AgentStatusBadge } from "./AgentStatusBadge";

interface AgentEvent {
  type: "agent_start" | "agent_complete" | "done" | "error";
  agent?: string;
  data?: Record<string, unknown>;
  goal_id?: string;
  report?: string;
}

interface Props {
  goalId: string;
}

export function AgentStreamPanel({ goalId }: Props) {
  const router = useRouter();
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [done, setDone] = useState(false);

  useEffect(() => {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/api/goals/${goalId}/stream`;
    const sse = new EventSource(url);

    const handleEvent = (type: AgentEvent["type"]) => (e: MessageEvent) => {
      const data = JSON.parse(e.data);
      setEvents((prev) => [...prev, { type, ...data }]);
      if (type === "done") {
        setDone(true);
        sse.close();
        setTimeout(() => router.push(`/goals/${goalId}`), 2000);
      }
    };

    sse.addEventListener("agent_start", handleEvent("agent_start"));
    sse.addEventListener("agent_complete", handleEvent("agent_complete"));
    sse.addEventListener("done", handleEvent("done"));
    sse.addEventListener("error", handleEvent("error"));

    return () => sse.close();
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
      {!events.length && (
        <div className="flex items-center gap-3 text-slate-400">
          <span className="animate-spin">⟳</span>
          <span>Connecting to AI agents...</span>
        </div>
      )}
    </div>
  );
}
