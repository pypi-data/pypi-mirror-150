//@ts-nocheck
import React, { useCallback, useRef } from 'react';
import Card from '@mui/material/Card';
import Grid from '@mui/material/Grid';
import CardContent from '@mui/material/CardContent';
import Box from '@mui/material/Box';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { IKeyframe } from '../widgetTypings';
import { Image } from 'image-js';

import { useDrag, useDrop } from 'react-dnd';

interface IKeyFrameCardProps {
  keyframe: IKeyframe;
}

export function KeyframeCard(props: IKeyFrameCardProps) {
  const { keyframe } = props;
  const keyframeCoordinates = keyframe.coordinates;
  const newImage = new Image(100, 100, keyframe.image, { kind: 'RGB' as any })
    .resize({ factor: 2 })
    .toDataURL();

  return (
    <div style={{ paddingTop: '8px', paddingBottom: '8px' }}>
      <Card sx={{ display: 'flex' }}>
        <Grid container justifyContent={'space-between'}>
          <Grid item>
            <Box sx={{ display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flex: '1 0 auto' }}>
                <Typography variant="body2" color="text.secondary">
                  Theta: {keyframeCoordinates.theta}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Phi: {keyframeCoordinates.phi}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Radius: {keyframeCoordinates.radius}
                </Typography>
              </CardContent>
            </Box>
          </Grid>
          <Grid item>
            <CardMedia
              height={'100%'}
              component="img"
              sx={{ width: 100 }}
              image={newImage}
              alt="Live from space album cover"
            />
          </Grid>
        </Grid>
      </Card>
    </div>
  );
}
