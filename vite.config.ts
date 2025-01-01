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
  root: resolve("./laid_out/static/src/"),
  base: "/static/",
  css: {
    postcss: postcssConfig,
  },
  server: {
    host: "0.0.0.0",
    // port: 3000,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  build: {
    outDir: resolve("./laid_out/static/dist"),
    assetsDir: "",
    manifest: true,
    emptyOutDir: true,
    target: "es2015",
    rollupOptions: {
      input: {
        anxiety: resolve("./laid_out/static/src/ts/anxiety/anxiety.ts"),
        goal: resolve("./laid_out/static/src/ts/goal/goal.ts"),
        gratitude: resolve("./laid_out/static/src/ts/gratitude/gratitude.ts"),
        journal: resolve("./laid_out/static/src/ts/journal/journal.ts"),
        style: resolve("./laid_out/static/src/ts/style.ts"),
      },
      output: {
        chunkFileNames: undefined,
      },
    },
  },
});
