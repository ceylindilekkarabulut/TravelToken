import type { Metadata } from "next";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { WalletProvider } from "@/components/wallet/WalletProvider";
import { Toaster } from "sonner";

export const metadata: Metadata = {
  title: "Throne Travel",
  description: "AI-powered travel planning on Solana",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body>
        <WalletProvider>
          <Navbar />
          <main className="min-h-screen">{children}</main>
          <Footer />
          <Toaster richColors position="top-right" />
        </WalletProvider>
      </body>
    </html>
  );
}
