"use client";

import Link from "next/link";
import { WalletButton } from "@/components/wallet/WalletButton";
import { Plane } from "lucide-react";

export function Navbar() {
  return (
    <nav className="border-b border-surface-border bg-surface/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 font-bold text-xl">
          <Plane className="text-brand-light" size={24} />
          <span className="bg-gradient-to-r from-brand-light to-purple-300 bg-clip-text text-transparent">
            Throne Travel
          </span>
        </Link>
        <div className="flex items-center gap-6">
          <Link href="/routes/search" className="text-slate-400 hover:text-slate-200 transition-colors">
            Discover
          </Link>
          <Link href="/create" className="text-slate-400 hover:text-slate-200 transition-colors">
            Create Goal
          </Link>
          <WalletButton />
        </div>
      </div>
    </nav>
  );
}
