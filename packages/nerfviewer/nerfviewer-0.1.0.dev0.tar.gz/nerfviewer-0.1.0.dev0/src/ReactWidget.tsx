/* eslint-disable @typescript-eslint/no-unused-vars */
import React, { useState } from 'react';
import { WidgetModel } from '@jupyter-widgets/base';
import { useModelState, WidgetModelContext } from './hooks/widget-model';
import Navigator from './components/Navigator';
import Viewer from './components/Viewer';
import ResponsiveAppBar from './components/AppBar';
import { IViewTypes } from './widgetTypings';

interface WidgetProps {
  model: WidgetModel;
  view: IViewTypes;
}

function ReactWidget(props: WidgetProps) {
  const [view, setView] = useState(props.view);
  // Global state for current positioning of the camera
  // const [cameraPosition, setCameraPosition] = useModelState(
  //   'currentCameraPosition'
  // );

  // const [textToDisplay] = useModelState('value');
  // const [foo] = useModelState('foo');
  //const [path, setPath] = useState<IPathDatum[]>([]);

  const [{ theta, phi, radius }, setCameraPosition] =
    useModelState('cameraCoordinates');

  const [imageArray] = useModelState('imageArray');
  const [keyframes, setKeyFrames] = useModelState('keyframes');
  const [videoNum, setVideoNum] = useModelState('videoNum');
  //const [playNum, setPlayNum] = useModelState('playNum');
  const [videoString, setVideoString] = useModelState('videoString');

  console.log(keyframes);
  return (
    <div>
      <ResponsiveAppBar setView={setView} />
      {view === 'navigation' && (
        <Navigator
          cameraPosition={{ theta, phi, radius }}
          setCameraPosition={setCameraPosition}
          /* TODO: should not hardcode these */
          image={imageArray}
          keyframes={keyframes}
          setKeyFrames={setKeyFrames}
        />
      )}
      {view === 'rendering' && (
        <Viewer
          videoNum={videoNum}
          setVideoNum={setVideoNum}
          videoString={videoString}
          setVideoString={setVideoString}
        ></Viewer>
      )}
      {/* <p>{imageArray.length}</p>

      playNum={playNum}
          setPlayNum={setPlayNum}


      <p>{Math.max(...imageArray)}</p> */}
      {/* {console.log(keyframes)} */}

      {/* <p>{textToDisplay}</p>
      <p>{foo}</p>
      <p>{foo}</p>
      <p>{foo}</p>
      <p>{theta}</p>
      <p>{phi}</p>
      <p>{radius}</p> */}
    </div>
  );
}

function withModelContext(Component: (props: WidgetProps) => JSX.Element) {
  return (props: WidgetProps) => (
    <WidgetModelContext.Provider value={props.model}>
      <Component {...props} />
    </WidgetModelContext.Provider>
  );
}

export default withModelContext(ReactWidget);
