import { io } from "socket.io-client";

export const socket = new WebSocket(import.meta.env.VITE_API_SERVER_SOCKET_URL);
