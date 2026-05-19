import { create } from "zustand";

interface WalletStore {
  wallet: string | null;
  setWallet: (w: string | null) => void;
}

export const useWalletStore = create<WalletStore>((set) => ({
  wallet: null,
  setWallet: (wallet) => set({ wallet }),
}));
