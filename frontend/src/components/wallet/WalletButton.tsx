"use client";

import { useWallet } from "@solana/wallet-adapter-react";
import { useWalletModal } from "@solana/wallet-adapter-react-ui";
import { useWalletStore } from "@/stores/walletStore";
import { useEffect } from "react";

export function WalletButton() {
  const { publicKey, disconnect, connected } = useWallet();
  const { setVisible } = useWalletModal();
  const { setWallet } = useWalletStore();

  useEffect(() => {
    setWallet(publicKey?.toBase58() ?? null);
  }, [publicKey, setWallet]);

  if (connected && publicKey) {
    return (
      <button
        onClick={disconnect}
        className="bg-surface-card border border-surface-border px-4 py-1.5 rounded-lg text-sm font-mono hover:border-brand transition-colors"
      >
        {publicKey.toBase58().slice(0, 4)}...{publicKey.toBase58().slice(-4)}
      </button>
    );
  }

  return (
    <button
      onClick={() => setVisible(true)}
      className="bg-brand text-white px-4 py-1.5 rounded-lg text-sm font-semibold hover:bg-brand-dark transition-colors"
    >
      Connect Wallet
    </button>
  );
}
