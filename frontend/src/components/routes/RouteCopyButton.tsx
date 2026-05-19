"use client";

import { useState } from "react";
import { Copy, Check } from "lucide-react";
import { api } from "@/lib/api";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

interface Props {
  routeId: string;
}

export function RouteCopyButton({ routeId }: Props) {
  const [copied, setCopied] = useState(false);
  const router = useRouter();

  const handleCopy = async () => {
    await api.copyRoute(routeId);
    setCopied(true);
    toast.success("Route copied to your goals!");
    setTimeout(() => setCopied(false), 2000);
    // also navigate to create page prefilled with route info
    // fetch route details (best-effort) and prefill create form
    try {
      const r = await fetch(`/api/routes/${routeId}`).then((r) => r.json()).catch(() => null);
      if (r && (r.origin || r.destination)) {
        const params = new URLSearchParams();
        if (r.origin) params.set("origin", r.origin);
        if (r.destination) params.set("destination", r.destination);
        router.push(`/create?${params.toString()}`);
      }
    } catch (e) {
      // ignore
    }
  };

  return (
    <button
      onClick={handleCopy}
      className="flex items-center gap-1.5 text-sm border border-surface-border rounded-lg px-3 py-1.5 hover:border-brand transition-colors"
    >
      {copied ? <Check size={14} className="text-green-400" /> : <Copy size={14} />}
      {copied ? "Copied!" : "Copy"}
    </button>
  );
}
