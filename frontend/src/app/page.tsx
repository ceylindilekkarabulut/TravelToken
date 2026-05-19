"use client";

import { useState } from "react";
import CreateGoalModal from "@/components/CreateGoalModal";

export default function HomePage() {
  const [showModal, setShowModal] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-4 py-20">
        {/* Hero Section */}
        <section className="text-center mb-20">
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400 bg-clip-text text-transparent">
            Throne Travel
          </h1>
          <p className="text-2xl text-slate-300 mb-2">AI-Powered Travel Planning</p>
          <p className="text-lg text-slate-400 mb-12">
            Create goals, get AI analysis, find sponsors, make it real
          </p>

          <button
            onClick={() => setShowModal(true)}
            className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-8 py-4 rounded-xl font-bold text-lg transition-all transform hover:scale-105 shadow-lg"
          >
            ✨ Create Travel Goal
          </button>
        </section>

        {/* Features */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <div className="bg-slate-800/50 backdrop-blur border border-purple-500/20 rounded-lg p-6 hover:border-purple-500/50 transition">
            <div className="text-3xl mb-3">🤖</div>
            <h3 className="font-bold text-lg mb-2 text-purple-300">AI Agents</h3>
            <p className="text-slate-400">Route planning, deal hunting, budget optimization</p>
          </div>

          <div className="bg-slate-800/50 backdrop-blur border border-pink-500/20 rounded-lg p-6 hover:border-pink-500/50 transition">
            <div className="text-3xl mb-3">🌐</div>
            <h3 className="font-bold text-lg mb-2 text-pink-300">Community</h3>
            <p className="text-slate-400">Get sponsors, share goals, build together</p>
          </div>

          <div className="bg-slate-800/50 backdrop-blur border border-purple-500/20 rounded-lg p-6 hover:border-purple-500/50 transition">
            <div className="text-3xl mb-3">⛓️</div>
            <h3 className="font-bold text-lg mb-2 text-purple-300">Blockchain</h3>
            <p className="text-slate-400">Secure escrow, transparent transactions</p>
          </div>
        </section>

        {/* Demo Status */}
        <section className="mt-20 max-w-2xl mx-auto">
          <div className="bg-slate-800/50 backdrop-blur border border-green-500/30 rounded-lg p-8">
            <h2 className="text-xl font-bold text-green-400 mb-4">✓ Demo Status</h2>
            <div className="space-y-2 text-sm text-slate-300">
              <p>✓ Backend API connected</p>
              <p>✓ AI agents running</p>
              <p>✓ Database ready</p>
              <p>✓ Solana integration prepared</p>
            </div>
          </div>
        </section>
      </div>

      {showModal && <CreateGoalModal onClose={() => setShowModal(false)} />}
    </div>
  );
}

