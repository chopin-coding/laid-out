import {defineConfig} from "vite";
import vue from "@vitejs/plugin-vue";

import {resolve} from "path";

const postcssConfig = {
    plugins: [
        require("postcss-import")(),
        require("tailwindcss/nesting")(),
        require("tailwindcss")(),
        require("autoprefixer")(),
    ],
};

export default defineConfig({
    plugins: [vue()],
    root: resolve("./static/src"),
    base: "/static/",
    css: {
        postcss: postcssConfig,
    },
    server: {
        host: "0.0.0.0",
        port: 3000,
        open: false,
        watch: {
            usePolling: true,
            disableGlobbing: false,
        },
    },
    build: {
        outDir: resolve("./static/dist"),
        assetsDir: "",
        manifest: true,
        emptyOutDir: true,
        target: "es2015",
        rollupOptions: {
            input: {
                main: resolve("./static/src/ts/main.ts"),
                style: resolve("./static/src/ts/style.ts"),
            },
            output: {
                chunkFileNames: undefined,
            },
        },
    },
});
