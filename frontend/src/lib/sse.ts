export function createSSEConnection(url: string, handlers: Record<string, (data: unknown) => void>) {
  const sse = new EventSource(url);
  for (const [event, handler] of Object.entries(handlers)) {
    sse.addEventListener(event, (e: MessageEvent) => handler(JSON.parse(e.data)));
  }
  return sse;
}
