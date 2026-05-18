import { create } from "zustand";

interface Notification {
  message: string;
  onApprove?: () => void;
}

interface NotificationStore {
  notification: Notification | null;
  setNotification: (n: Notification) => void;
  clearNotification: () => void;
}

export const useNotificationStore = create<NotificationStore>((set) => ({
  notification: null,
  setNotification: (notification) => set({ notification }),
  clearNotification: () => set({ notification: null }),
}));
