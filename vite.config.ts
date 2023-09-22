import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

import {resolve} from "path";


export default defineConfig({
  plugins: [vue()],
  root: resolve("./static/src"),
  base: "/static/",
  server: {
    host: "0.0.0.0",
    port: 3000,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  resolve: {
    extensions: [".js", ".ts", ".json"],
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
      },
      output: {
        chunkFileNames: undefined,
      },
    },
  },
});
