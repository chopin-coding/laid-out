export interface Sprite {
  render: Function;
  update: Function;
}

export interface Action {
  name: string;
  probabilityMultiplier: number;
  numberOfFrames: number;
  ticksPerFrame: number;
  loop: boolean;
}

export interface AnimationOptions {
  context: CanvasRenderingContext2D;
  width: number;
  height: number;
  image: any;
  action: Action
}
