export interface Body {
  id: number;
  simulationId: number;
  mass: number;
  initialPosition: { x: number; y: number };
  initialVelocity: { x: number; y: number };
  modelPath: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface BodyState {
  bodyId: number;
  positionX: number;
  positionY: number;
  velocityX: number;
  velocityY: number;
}
