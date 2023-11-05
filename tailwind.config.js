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


        },
        extend: {
            boxShadow: {
                inputShadowBottom: 'inset 0px -2px 6px -2px rgba(0, 0, 0, 0.1)',
            }
        },
    },
    plugins: [],
};
