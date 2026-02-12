import { defineConfig } from "vite";
import ui from "@nuxt/ui/vite";
import { fileURLToPath } from "url";

export default defineConfig({
  build: {
    emptyOutDir: true,
    outDir: "../server_flask/app/static",
  },
  plugins: [
    ui({
      ui: {
        colors: {
          primary: "blue",
          neutral: "gray",
        },
        formField: {
          slots: {
            root: "mb-3",
          },
        },
        fonts: false,
        input: {
          slots: {
            root: "w-full",
          },
        },
        modal: {
          slots: {
            header: "p-3",
            content: "sm:max-w-xl",
          },
        },
        pageHeader: {
          slots: {
            root: "relative border-none py-4",
            title: "text-2xl sm:text-3xl text-red-800",
          },
        },
        textarea: {
          slots: {
            root: "w-full",
          },
        },
      },
    }),
  ],
  resolve: {
    alias: {
      "@/": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    host: "localhost",
    port: 5000,
    proxy: {
      "/routes": {
        target: "http://127.0.0.1:5000/routes/*",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/routes/, ""),
      },
    },
  },
});
