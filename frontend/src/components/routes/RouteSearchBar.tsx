import { Search } from "lucide-react";

interface Props {
  value: string;
  onChange: (v: string) => void;
}

export function RouteSearchBar({ value, onChange }: Props) {
  return (
    <div className="relative">
      <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search routes: Istanbul to Paris, beach Europe..."
        className="w-full bg-surface-card border border-surface-border rounded-xl pl-12 pr-4 py-3 focus:ring-2 focus:ring-brand outline-none"
      />
    </div>
  );
}
