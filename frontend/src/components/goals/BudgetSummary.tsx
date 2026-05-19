interface Props {
  estimated?: number | null;
  budget?: number | null;
}

export function BudgetSummary({ estimated, budget }: Props) {
  if (estimated == null && budget == null) return null;

  return (
    <div className="bg-surface-card border border-surface-border rounded-xl p-4 mt-4">
      <h4 className="font-semibold mb-2">Budget Summary</h4>
      <div className="flex items-center justify-between text-sm text-slate-400">
        <span>Estimated cost</span>
        <span className="font-medium text-slate-200">{estimated != null ? `$${estimated.toFixed(2)}` : "—"}</span>
      </div>
      <div className="flex items-center justify-between text-sm text-slate-400 mt-1">
        <span>Your budget</span>
        <span className="font-medium text-slate-200">{budget != null ? `$${budget.toFixed(2)}` : "—"}</span>
      </div>
      {estimated != null && budget != null && (
        <div className="mt-3 text-sm">
          {estimated <= budget ? (
            <p className="text-green-300">Within budget ✅</p>
          ) : (
            <p className="text-red-400">Over budget by ${ (estimated - budget).toFixed(2) }</p>
          )}
        </div>
      )}
    </div>
  );
}
