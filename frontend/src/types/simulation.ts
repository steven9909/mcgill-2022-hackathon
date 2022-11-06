import { Body } from "./body";

export interface Simulation {
  id: number;
  name: string;
  createdAt: Date;
  updatedAt: Date;
  bodies: Record<string, Body>;
}
