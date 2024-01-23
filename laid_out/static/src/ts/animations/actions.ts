export const actions = {
  cat_01: [
    {
      name: "base",
      probabilityMultiplier: 4,
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
    {
      name: "paw",
      probabilityMultiplier: 1,
      numberOfFrames: 1,
      ticksPerFrame: 110,
      loop: false
    },
    {
      name: "tail",
      probabilityMultiplier: 1,
      numberOfFrames: 1,
      ticksPerFrame: 110,
      loop: false
    },
  ]
};
