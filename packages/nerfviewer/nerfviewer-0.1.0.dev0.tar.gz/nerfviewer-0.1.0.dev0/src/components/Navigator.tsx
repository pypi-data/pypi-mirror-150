import { Button, Slider } from '@mui/material';
import React, { useState, useEffect } from 'react';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Tooltip from '@mui/material/Tooltip';

import { ICoordinates, IKeyframe } from '../widgetTypings';
import { Image } from 'image-js';

import KeyframeList from './KeyframeList';
interface INavigatorProps {
  cameraPosition: ICoordinates;
  setCameraPosition: any;
  image: number[];
  keyframes: IKeyframe[]; //[];
  setKeyFrames: any;
}
const Navigator = (props: INavigatorProps): JSX.Element => {
  const [isImageLoading, setIsImageLoading] = useState(false);
  const { keyframes, image, setCameraPosition, setKeyFrames } = props;

  useEffect(() => {
    setIsImageLoading(false);
  }, [image]);

  function updateCameraPosition(
    variable: 'phi' | 'theta' | 'radius',
    value: number
  ) {
    setIsImageLoading(true);
    const newCameraPosition: ICoordinates = {
      ...props.cameraPosition,
    };

    newCameraPosition[variable] = value;
    setCameraPosition(newCameraPosition);
  }
  const newImage = new Image(100, 100, image, { kind: 'RGB' as any });
  return (
    <div>
      <Grid container spacing={2}>
        <Grid item xs={7} md={7}>
          <Grid md={12}>
            <div>
              Theta
              <Slider
                min={0}
                defaultValue={100}
                max={360}
                aria-label="Default"
                valueLabelDisplay="auto"
                onChange={(_, theta) =>
                  updateCameraPosition('theta', theta as number)
                }
              />
              Phi
              <Slider
                min={-90}
                defaultValue={-30}
                max={0}
                aria-label="Default"
                valueLabelDisplay="auto"
                onChange={(_, phi) =>
                  updateCameraPosition('phi', phi as number)
                }
              />
              Radius
              <Slider
                step={0.1}
                min={3}
                defaultValue={4}
                max={5}
                aria-label="Default"
                valueLabelDisplay="auto"
                onChange={(_, radius) =>
                  updateCameraPosition('radius', radius as number)
                }
              />
            </div>
          </Grid>

          <Grid item xs={12} md={12}>
            <Box
              component="img"
              sx={{
                height: 500,
                width: 500,
                maxHeight: { xs: 700, md: 700 },
                maxWidth: { xs: 700, md: 700 },
              }}
              style={isImageLoading ? { opacity: 0.7 } : {}}
              alt="The house from the offer."
              src={newImage.resize({ factor: 2 }).toDataURL()}
            />
          </Grid>

          <Grid md={12}>
            <Tooltip
              title={isImageLoading ? 'Loading new frame' : 'Save Keyframe'}
            >
              <Button
                variant="contained"
                disabled={isImageLoading}
                onClick={() => {
                  const clonedKeyframes = [...(props.keyframes || [])];
                  clonedKeyframes.push({
                    image: props.image,
                    coordinates: props.cameraPosition,
                  });
                  props.setKeyFrames(clonedKeyframes);
                }}
              >
                Save Frame
              </Button>
            </Tooltip>
          </Grid>
        </Grid>
        <Grid item xs={5} md={5}>
          <KeyframeList keyframes={keyframes} setKeyFrames={setKeyFrames} />
        </Grid>
      </Grid>
    </div>
  );
};

export default Navigator;
