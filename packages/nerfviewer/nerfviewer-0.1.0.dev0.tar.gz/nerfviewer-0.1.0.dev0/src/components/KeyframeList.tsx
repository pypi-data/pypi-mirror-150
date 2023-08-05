//@ts-nocheck
import React, { useCallback } from 'react';

import { IKeyframe } from '../widgetTypings';
import { KeyframeCard } from './KeyframeCard';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

import HTML5Backend from 'react-dnd-html5-backend'; /*
Sample keyframe props
[
    {
      image: 'https://mui.com/static/images/cards/contemplative-reptile.jpg',
      coordinates: {
        theta: 100,
        phi: -30,
        radius: 4,
      },
    },
    {
      image: 'https://mui.com/static/images/cards/contemplative-reptile.jpg',
      coordinates: {
        theta: 80,
        phi: -20,
        radius: 2,
      },
    },
  ]

*/
import { Button } from '@mui/material';

interface IKeyFrameListProps {
  keyframes: IKeyframe[];
  setKeyFrames: any;
}

export default function KeyframeList(props: IKeyFrameListProps) {
  const { keyframes, setKeyFrames } = props;

  const moveCard = useCallback(
    (dragIndex, hoverIndex) => {
      const dragCard = keyframes[dragIndex];
      const keyframeCopy = [...keyframes];
      keyframeCopy.splice(dragIndex, 1); // removing what you are dragging.
      keyframeCopy.splice(hoverIndex, 0, dragCard); // inserting it into hoverIndex.
      setKeyFrames(keyframeCopy);
    },
    [keyframes]
  );

  function reorder(startIndex: number, endIndex: number) {
    const result = Array.from(keyframes);
    const [removed] = result.splice(startIndex, 1);
    result.splice(endIndex, 0, removed);

    return result;
  }

  function onDragEnd(result) {
    // dropped outside the list
    if (!result.destination) {
      return;
    }

    moveCard(result.source.index, result.destination.index);
  }

  return (
    <div>
      <DragDropContext onDragEnd={onDragEnd}>
        <Droppable droppableId="droppable">
          {(provided, snapshot) => (
            <div {...provided.droppableProps} ref={provided.innerRef}>
              {keyframes &&
                keyframes.map((item, index) => (
                  <Draggable
                    key={JSON.stringify(item.coordinates)}
                    draggableId={JSON.stringify(item.coordinates)}
                    index={index}
                  >
                    {(provided, snapshot) => (
                      <div
                        ref={provided.innerRef}
                        style={{ 'margin-bottom': '5px' }}
                        {...provided.draggableProps}
                        {...provided.dragHandleProps}
                      >
                        <KeyframeCard keyframe={item}></KeyframeCard>
                      </div>
                    )}
                  </Draggable>
                ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>
      <div style={{ paddingTop: '16px' }}>
        {keyframes && keyframes.length > 0 && (
          <Button
            contained
            onClick={() => {
              let keyframeCopy = [...keyframes];
              keyframeCopy = keyframeCopy.map((keyframe) => {
                keyframe.image = [];
                return keyframe;
              });
              copyText(JSON.stringify(keyframeCopy));
            }}
          >
            Copy Keyframes
          </Button>
        )}
      </div>
    </div>
  );
}

async function copyText(text) {
  if (navigator.clipboard) {
    await navigator.clipboard.writeText(text);
    return;
  }
}
