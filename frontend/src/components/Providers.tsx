"use client";

import { useEffect, useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { WalletProvider } from "@/components/wallet/WalletProvider";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Toaster } from "sonner";
import { DealNotificationModal } from "@/components/agents/DealNotificationModal";
import { NotificationBridge } from "@/components/NotificationBridge";

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <WalletProvider>
        <Navbar />
        <NotificationBridge />
        {children}
        <Footer />
        <DealNotificationModal />
        <Toaster richColors position="top-right" />
      </WalletProvider>
    </QueryClientProvider>
  );
}
