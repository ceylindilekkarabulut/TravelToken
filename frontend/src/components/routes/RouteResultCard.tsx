import { MapPin, Copy } from "lucide-react";
import { RouteCopyButton } from "./RouteCopyButton";
import type { RouteResponse } from "@/types/api";

interface Props {
  route: RouteResponse;
}

export function RouteResultCard({ route }: Props) {
  return (
    <div className="bg-surface-card border border-surface-border rounded-xl p-5 flex items-start justify-between gap-4">
      <div className="flex-1">
        <div className="flex items-center gap-2 mb-2">
          <MapPin size={16} className="text-brand-light" />
          <span className="font-semibold">{route.origin} → {route.destination}</span>
        </div>
        <p className="text-slate-400 text-sm">{route.description_md}</p>
        <p className="text-xs text-slate-500 mt-2">{route.copy_count} copies</p>
      </div>
      <RouteCopyButton routeId={route.id} />
    </div>
  );
}
