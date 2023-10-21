/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./templates/*/*.{vue,ts,html,css}",
      "./templates/*.{vue,ts,html,css}",
    "./anxiety/templates/*/*.{vue,ts,html,css}",
    "./static/src/*/*.{vue,ts,html,css}",
  ],
  theme: {
    colors: {
      textwhite: "rgb(var(--color-textwhite) / 1)",
      textwhitedim: "rgb(var(--color-textwhite) / .8)",

      textblack: "rgb(var(--color-textblack) / 1)",
      textblackdim: "rgb(var(--color-textblack) / .9)",

      white: "rgb(var(--color-white) / 1)",
      black: "rgb(var(--color-black) / 1)",

      backg: "rgb(var(--color-backg) / 1)",

      primary: "rgb(var(--color-primary) / 1)",
      primaryshade: "rgb(var(--color-primary) / .8)",
      primarylight: "rgb(var(--color-primary) / .05)",

      secondary: "rgb(var(--color-secondary) / 1)",

      accent: "rgb(var(--color-accent) / 1)",
      accentshade: "rgb(var(--color-accent) / .2)",
    },
    // fontFamily: {
    //   sans: ["Poppins", ...defaultTheme.fontFamily.sans],
    //   serif: ["Poppins", "serif"],
    // },
    // fontWeight: {
    //   thin: "100",
    //   extralight: "200",
    //   light: "300",
    //   normal: "400",
    //   medium: "500",
    //   semibold: "600",
    //   bold: "700",
    //   extrabold: "800",
    //   black: "900",
    // },
    extend: {},
  },
  plugins: [],
};

// @import url('https://fonts.googleapis.com/css?family=Lato:700|Lato:400');
//
// body {
//   font-family: 'Lato';
//   font-weight: 400;
// }
//
// h1, h2, h3, h4, h5 {
//   font-family: 'Lato';
//   font-weight: 700;
// }
//
// html {font-size: 100%;} /* 16px */
//
// h1 {font-size: 3.053rem; /* 48.8px */}
//
// h2 {font-size: 2.442rem; /* 39.04px */}
//
// h3 {font-size: 1.954rem; /* 31.2px */}
//
// h4 {font-size: 1.563rem; /* 24.96px */}
//
// h5 {font-size: 1.250rem; /* 20px */}
//
// small {font-size: 0.800rem; /* 12.8px */}
