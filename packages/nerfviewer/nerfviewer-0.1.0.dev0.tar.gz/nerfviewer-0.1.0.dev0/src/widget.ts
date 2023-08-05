// Copyright (c) Dylan Wootton and Josh Pollock
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';
import ReactWidget from './ReactWidget';
import React from 'react';
import ReactDOM from 'react-dom';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';
import { ICoordinates, IKeyframe } from './widgetTypings';

// Your widget state goes here. Make sure to update the corresponding
// Python state in example.py

export type WidgetModelState = {
  value: string;
  color: string;
  view: string;
  cameraCoordinates: ICoordinates;
  foo: string;
  imageArray: number[];
  keyframes: IKeyframe[]; // TODO change to Ikeyframes when we have image piped through
  videoNum: number;
  playNum: number;
  videoString?: string;
};

export class ExampleModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: ExampleModel.model_name,
      _model_module: ExampleModel.model_module,
      _model_module_version: ExampleModel.model_module_version,
      _view_name: ExampleModel.view_name,
      _view_module: ExampleModel.view_module,
      _view_module_version: ExampleModel.view_module_version,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'ExampleModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'ExampleView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class ExampleView extends DOMWidgetView {
  render() {
    this.el.classList.add('custom-widget');

    const component = React.createElement(ReactWidget, {
      model: this.model,
      view: 'home',
    });
    ReactDOM.render(component, this.el);
  }
}
