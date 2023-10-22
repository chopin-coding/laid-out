/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./templates/*/*.{ts,html,css}",
      "./templates/*.{ts,html,css}",
    "./anxiety/templates/*/*.{ts,html,css}",
    "./static/src/*/*.{vue,ts,html,css}",
      "./static/src/ts/*/*.{vue,ts,html,css}",
  ],
  theme: {
    colors: {
      textwhite: "rgb(var(--color-textwhite) / 1)",
      textwhitedim: "rgb(var(--color-textwhite) / .8)",

      textblack: "rgb(var(--color-textblack) / 1)",
      textblackdim: "rgb(var(--color-textblack) / .9)",
      textblackdimmer: "rgb(var(--color-textblack) / .7)",

      white: "rgb(var(--color-white) / 1)",
      black: "rgb(var(--color-black) / 1)",

      backg: "rgb(var(--color-backg) / 1)",

      primary: "rgb(var(--color-primary) / 1)",
      primaryshade: "rgb(var(--color-primary) / .8)",
      primarylight: "rgb(var(--color-primary) / .1)",

      secondary: "rgb(var(--color-secondary) / 1)",

      accent: "rgb(var(--color-accent) / 1)",
      accentshade: "rgb(var(--color-accent) / .2)",
    },
    extend: {},
  },
  plugins: [],
};
