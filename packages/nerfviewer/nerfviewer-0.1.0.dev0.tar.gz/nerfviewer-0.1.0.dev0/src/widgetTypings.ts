export interface IKeyframe {
  image: number[];
  coordinates: ICoordinates;
}

export interface ICoordinates {
  theta: number;
  phi: number;
  radius: number;
}

export type IViewTypes = 'navigation' | 'rendering' | 'home';
