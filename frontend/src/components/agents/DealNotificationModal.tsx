"use client";

import { useNotificationStore } from "@/stores/notificationStore";
import { motion, AnimatePresence } from "framer-motion";

export function DealNotificationModal() {
  const { notification, clearNotification } = useNotificationStore();

  return (
    <AnimatePresence>
      {notification && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          className="fixed bottom-8 right-8 bg-surface-card border border-green-700 rounded-2xl p-6 max-w-sm shadow-2xl z-50"
        >
          <div className="flex items-start gap-3">
            <span className="text-2xl">🔥</span>
            <div className="flex-1">
              <p className="font-semibold text-green-300">Deal Alert!</p>
              <p className="text-sm text-slate-300 mt-1">{notification.message}</p>
              <div className="flex gap-2 mt-4">
                <button
                  onClick={() => notification.onApprove?.()}
                  className="flex-1 bg-green-700 text-white py-1.5 rounded-lg text-sm font-semibold hover:bg-green-600 transition-colors"
                >
                  Approve
                </button>
                <button
                  onClick={clearNotification}
                  className="flex-1 border border-surface-border py-1.5 rounded-lg text-sm hover:bg-surface transition-colors"
                >
                  Dismiss
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
