interface AnimationOptions {
  context: CanvasRenderingContext2D;
  width: number;
  height: number;
  image: any;
  numberOfFrames: number;
  ticksPerFrame: number;
  loop: boolean;
}

export const sprite = (options: AnimationOptions) => {
    let frameIndex = 0; // The current frame to be displayed
    let tickCount = 0; // The number updates since the current frame was first displayed

    const {
      context,
      width,
      height,
      image,
      numberOfFrames,
      ticksPerFrame,
      loop,
    } =
      options;
    const scaleFactor = calculateScaleFactor();

    //get the canvas, canvas context, and dpi
    let canvas = document.getElementById('myCanvas')
    let dpi = window.devicePixelRatio;

    function fixDpi() {
//create a style object that returns width and height
      let style = {
        _height() {
          return +getComputedStyle(canvas).getPropertyValue('height').slice(0, -2);
        }
        ,
        _width() {
          return +getComputedStyle(canvas).getPropertyValue('width').slice(0, -2);
        }
      }
      //set the correct attributes for a crystal clear image!
      canvas.setAttribute('width', (style._width() * dpi).toString());
      canvas.setAttribute('height', (style._height() * dpi).toString());
    }

    function calculateScaleFactor() {
      const screenWidth = window.innerWidth;

      if (screenWidth <= 600) {
        return 1;
      } else {
        return 0.4;
      }
    }

    return {
      render: function () {
        // clear the canvas
        context.clearRect(0, 0, width, height);

        fixDpi()
        // draw the image
        context.drawImage(
          image,
          frameIndex * width,
          0,
          width,
          height,
          0,
          0,
          width * scaleFactor,
          height * scaleFactor
        );
      },
      update: function () {
        tickCount += 1;

        if (tickCount > ticksPerFrame) {
          tickCount = 0;

          if (frameIndex < numberOfFrames - 1) {
            frameIndex += 1;
          } else if (loop) {
            frameIndex = 0;
          }
        }
      },
    };
  }
;
