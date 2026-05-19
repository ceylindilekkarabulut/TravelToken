const WS_BASE = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

export function connectNotificationSocket(
  wallet: string,
  onMessage: (data: unknown) => void
): WebSocket {
  const ws = new WebSocket(`${WS_BASE}/ws/notifications/${wallet}`);
  ws.onmessage = (e) => onMessage(JSON.parse(e.data));
  return ws;
}
