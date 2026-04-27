import type { Message } from 'src/services/messaging';

export interface MessageCreatedEvent {
  type: 'message_created';
  conversation_id: number;
  message: Message;
}

export interface ConnectedEvent {
  type: 'connected';
}

export interface PongEvent {
  type: 'pong';
}

export type IncomingEvent = MessageCreatedEvent | ConnectedEvent | PongEvent;

type Listener = (event: IncomingEvent) => void;

class MessagingSocket {
  private ws: WebSocket | null = null;
  private listeners = new Set<Listener>();
  private reconnectAttempts = 0;
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private heartbeatTimer: ReturnType<typeof setInterval> | null = null;
  private intentionallyClosed = false;

  connect(): void {
    if (
      this.ws &&
      (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)
    ) {
      return;
    }

    this.intentionallyClosed = false;
    const url = this.buildUrl();
    this.ws = new WebSocket(url);

    this.ws.addEventListener('open', this.onOpen);
    this.ws.addEventListener('message', this.onMessage);
    this.ws.addEventListener('close', this.onClose);
    this.ws.addEventListener('error', this.onError);
  }

  disconnect(): void {
    this.intentionallyClosed = true;
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  on(listener: Listener): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  private buildUrl(): string {
    const base = (import.meta.env.VITE_WS_BASE as string | undefined) || this.defaultBase();
    return `${base}/ws/messages/`;
  }

  private defaultBase(): string {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    if (import.meta.env.DEV) {
      return `${protocol}//${window.location.hostname}:8000`;
    }
    return `${protocol}//${window.location.host}`;
  }

  private onOpen = () => {
    this.reconnectAttempts = 0;
    if (this.heartbeatTimer) clearInterval(this.heartbeatTimer);
    this.heartbeatTimer = setInterval(() => this.send({ type: 'ping' }), 30000);
  };

  private onMessage = (event: MessageEvent<string>) => {
    let data: IncomingEvent | null = null;
    try {
      data = JSON.parse(event.data) as IncomingEvent;
    } catch {
      return;
    }
    if (!data) return;
    for (const listener of this.listeners) {
      try {
        listener(data);
      } catch (err) {
        console.error('Messaging listener error:', err);
      }
    }
  };

  private onClose = (event: CloseEvent) => {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
    this.ws = null;

    if (this.intentionallyClosed) return;
    if (event.code === 4001) return;

    const delay = Math.min(30000, 1000 * Math.pow(2, this.reconnectAttempts));
    this.reconnectAttempts += 1;
    this.reconnectTimer = setTimeout(() => this.connect(), delay);
  };

  private onError = (event: Event) => {
    console.warn('Messaging WS error', event);
  };

  private send(payload: unknown): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) return;
    this.ws.send(JSON.stringify(payload));
  }
}

export const messagingSocket = new MessagingSocket();
