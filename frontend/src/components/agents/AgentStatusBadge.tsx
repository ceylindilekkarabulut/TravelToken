interface Props {
  type: "agent_start" | "agent_complete" | "done" | "error";
}

const config = {
  agent_start: { color: "bg-yellow-900 text-yellow-300", label: "Running" },
  agent_complete: { color: "bg-green-900 text-green-300", label: "Done" },
  done: { color: "bg-brand text-white", label: "Complete" },
  error: { color: "bg-red-900 text-red-300", label: "Error" },
};

export function AgentStatusBadge({ type }: Props) {
  const { color, label } = config[type];
  return (
    <span className={`text-xs px-2 py-1 rounded-full font-medium ${color}`}>{label}</span>
  );
}
