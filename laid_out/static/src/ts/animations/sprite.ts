import {AnimationOptions} from "./models";

export const sprite = (options: AnimationOptions) => {
    let frameIndex = 0; // The current frame to be displayed
    let tickCount = 0; // The number updates since the current frame was first displayed

    const {
      context,
      width,
      height,
      image,
      action,
    } =
      options;

    //get the canvas, canvas context, and dpi
    let canvas = document.getElementById('myCanvas')

    return {
      render: function () {
        context.clearRect(0, 0, width, height);

        context.drawImage(
          image,
          frameIndex * width,
          0,
          width,
          height,
          0,
          0,
          width,
          height
        );
      },
      update: function () {
        tickCount += 1;

        if (tickCount > action.ticksPerFrame) {
          tickCount = 0;

          if (frameIndex < action.numberOfFrames - 1) {
            frameIndex += 1;
          } else if (action.loop) {
            frameIndex = 0;
          }
        }
      },
    };
  }
;
