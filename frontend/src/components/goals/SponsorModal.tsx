"use client";

import { useState } from "react";
import { useWallet, useConnection } from "@solana/wallet-adapter-react";
import { SystemProgram, LAMPORTS_PER_SOL, Transaction, PublicKey } from "@solana/web3.js";
import { toast } from "sonner";
import { api } from "@/lib/api";

interface Props {
  open: boolean;
  onClose: () => void;
  goalId: string;
}

const TREASURY = new PublicKey("11111111111111111111111111111111");

export function SponsorModal({ open, onClose, goalId }: Props) {
  const [amount, setAmount] = useState("0.1");
  const [loading, setLoading] = useState(false);
  const { publicKey, sendTransaction } = useWallet();
  const { connection } = useConnection();

  if (!open) return null;

  const handleSponsor = async () => {
    if (!publicKey) { toast.error("Connect wallet first"); return; }
    setLoading(true);
    try {
      const lamports = parseFloat(amount) * LAMPORTS_PER_SOL;
      const tx = new Transaction().add(
        SystemProgram.transfer({ fromPubkey: publicKey, toPubkey: TREASURY, lamports })
      );
      const sig = await sendTransaction(tx, connection);
      await connection.confirmTransaction(sig, "confirmed");

      await api.createSponsorship({
        goal_id: goalId,
        sponsor_wallet: publicKey.toBase58(),
        amount_sol: parseFloat(amount),
        tx_signature: sig,
      });

      toast.success("Sponsored successfully!");
      onClose();
    } catch (e) {
      toast.error("Transaction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div className="bg-surface-card border border-surface-border rounded-2xl p-8 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6">Sponsor This Goal</h2>
        <label className="block text-sm font-medium mb-2">Amount (SOL)</label>
        <input
          type="number"
          step="0.01"
          min="0.01"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="w-full bg-surface border border-surface-border rounded-lg px-4 py-2 mb-6 focus:ring-2 focus:ring-brand outline-none"
        />
        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 border border-surface-border rounded-xl py-2 hover:bg-surface-card transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleSponsor}
            disabled={loading}
            className="flex-1 bg-brand text-white rounded-xl py-2 font-semibold hover:bg-brand-dark transition-colors disabled:opacity-50"
          >
            {loading ? "Sending..." : `Send ${amount} SOL`}
          </button>
        </div>
      </div>
    </div>
  );
}
