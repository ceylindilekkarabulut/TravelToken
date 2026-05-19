"use client";

interface Props extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export function Input({ label, className = "", ...props }: Props) {
  return (
    <div>
      {label && <label className="block text-sm font-medium mb-1">{label}</label>}
      <input
        {...props}
        className={`w-full bg-surface-card border border-surface-border rounded-md px-3 py-1.5 text-sm focus:ring-2 focus:ring-brand outline-none ${className}`}
      />
    </div>
  );
}
