/* eslint-disable @typescript-eslint/no-unused-vars */
import React from 'react';
import { HexColorPicker } from 'react-colorful';
import { useModelState } from './hooks/widget-model';

const ColorPicker = (): any => {
  const [color, setColor] = useModelState('color');

  return <HexColorPicker color={color} onChange={setColor}></HexColorPicker>;
};

export default ColorPicker;
