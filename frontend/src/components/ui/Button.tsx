"use client";

interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "ghost" | "primary";
}

export function Button({ variant = "default", className = "", ...props }: Props) {
  const base = "px-4 py-1.5 rounded-md text-sm font-semibold inline-flex items-center gap-2";
  const variants: Record<string, string> = {
    default: "bg-surface-card border border-surface-border text-slate-200",
    ghost: "bg-transparent text-slate-200",
    primary: "bg-brand text-white hover:bg-brand-dark",
  };

  return <button className={`${base} ${variants[variant]} ${className}`} {...props} />;
}
