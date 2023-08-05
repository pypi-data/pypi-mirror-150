import React, { useEffect, useState } from 'react';
import { Button, Grid } from '@mui/material';
interface IViewerProps {
  videoNum: number;
  setVideoNum?: any;
  // playNum: number;
  setVideoString?: any;
  videoString?: string;
}
const Viewer = ({
  setVideoNum,
  setVideoString,
  videoNum,
  // playNum,
  videoString,
}: IViewerProps) => {
  const [isViewerReady, setIsViewerReady] = useState(false);

  useEffect(() => {
    if (videoString) {
      setIsViewerReady(true);
    } else {
      setIsViewerReady(false);
    }
  }, [videoString]);

  return (
    <div>
      <Grid container justifyContent={'center'}>
        <Grid md={12}>
          <div>
            {/* eslint-disable-next-line no-extra-boolean-cast */}
            {isViewerReady ? (
              <video width={400} controls autoPlay loop>
                <source
                  src={'data:video/mp4;base64,' + videoString}
                  type={'video/mp4'}
                />
              </video>
            ) : (
              <video width={400} controls autoPlay loop></video>
            )}
          </div>
        </Grid>
        <Grid justifyContent={'space-between'} md={12}>
          <Button
            variant="contained"
            onClick={() => {
              setVideoNum(videoNum + 1);
            }}
          >
            Load Video
          </Button>
        </Grid>
      </Grid>
    </div>
  );
};

export default Viewer;
