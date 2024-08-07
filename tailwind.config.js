/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ['!**/node_modules', "./laid_out/templates/**/*.{html,css}", "./laid_out/templates/*.{html,css}", "./laid_out/anxiety/templates/**/*.{html,css}", "./laid_out/static/src/**/*.{html,css}", "./laid_out/static/src/ts/**/*.{vue,ts,html,css}", "./laid_out/static/src/ts/*.{vue,ts,html,css}",],
  theme: {
    colors: {
      textwhite: "rgb(var(--color-textwhite) / 1)",
      textwhitedim: "rgb(var(--color-textwhite) / .8)",
      textwhitedimmer: "rgb(var(--color-textwhite) / .7)",
      textwhitedimmer2: "rgb(var(--color-textwhite) / .3)",

      textblack: "rgb(var(--color-textblack) / 1)",
      textblackdim: "rgb(var(--color-textblack) / .9)",
      textblackdimmer: "rgb(var(--color-textblack) / .7)",
      textblackdimmer2: "rgb(var(--color-textblack) / .3)",
      textblackdimmest: "rgb(var(--color-textblack) / .15)",

      white: "rgb(var(--color-white) / 1)",
      black: "rgb(var(--color-black) / 1)",

      backg: "rgb(var(--color-backg) / 1)",

      primary: "rgb(var(--color-primary) / 1)",
      primaryshade: "rgb(var(--color-primary) / .8)",
      primarylight: "rgb(var(--color-primary) / .1)",

      secondary: "rgb(var(--color-secondary) / 1)",

      accent: "rgb(var(--color-accent) / 1)",
      accentshade: "rgb(var(--color-accent) / .2)",

      warning: "rgb(var(--color-warning) / 1)",

      danger: "rgb(var(--color-danger) / 1)"


    }, extend: {
      boxShadow: {
        inputShadowBottom: 'inset 0px -2px 6px -2px rgba(0, 0, 0, 0.1)',
      },

    },
  },
  plugins: [],
};
