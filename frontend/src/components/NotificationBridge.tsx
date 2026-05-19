"use client";

import { useEffect } from "react";
import { useWallet } from "@solana/wallet-adapter-react";
import { useNotificationStore } from "@/stores/notificationStore";
import { connectNotificationSocket } from "@/lib/ws";

export function NotificationBridge() {
  const { publicKey } = useWallet();
  const setNotification = useNotificationStore((state) => state.setNotification);

  useEffect(() => {
    if (!publicKey) return;
    const socket = connectNotificationSocket(publicKey.toBase58(), (data) => {
      if (typeof data === "object" && data && "message" in data) {
        setNotification({
          message: String((data as any).message),
        });
      }
    });

    return () => socket.close();
  }, [publicKey, setNotification]);

  return null;
}
