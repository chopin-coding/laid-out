export const actions = {
  cat_01: [
    {
      name: "base",
      probabilityMultiplier: 5,
      numberOfFrames: 1,
      ticksPerFrame: Math.floor(Math.random() * 301) + 300,
      loop: true
    },
    {
      name: "blink",
      probabilityMultiplier: 2,
      numberOfFrames: 1,
      ticksPerFrame: 80,
      loop: false
    },
    // {
    //   name: "breathe",
    //   probabilityMultiplier: 2,
    //   numberOfFrames: 1,
    //   ticksPerFrame: 300,
    //   loop: false
    // },
  ]
};
