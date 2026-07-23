import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import VueRouter from "vue-router/vite";
import ui from "@nuxt/ui/vite";

export default defineConfig({
  build: {
    emptyOutDir: true,
    outDir: "../server_flask/app/static",
  },
  plugins: [
    VueRouter(),
    vue(),
    ui({
      colorMode: false,
      icon: {
        clientBundle: {
          scan: true,
        },
      },
      ui: {
        colors: {
          error: "red",
          info: "cyan",
          neutral: "mist",
          secondary: "zinc",
          success: "emerald",
          primary: "blue",
          warning: "amber",
        },
        input: {
          slots: {
            root: "w-full",
          },
        },
        formField: {
          slots: {
            root: "mb-3",
          },
        },
        modal: {
          slots: {
            content: "md:max-w-2xl",
          },
        },
        pageBody: {
          base: "pb-4 my-4 space-y-4",
        },
        pageHeader: {
          slots: {
            root: "relative border-none mt-10",
            title: "text-2xl sm:text-3xl text-red-800",
          },
        },
        select: {
          slots: {
            base: "w-full",
          },
        },
        textarea: {
          slots: {
            root: "w-full",
          },
          variants: {
            autoresize: { true: "vertical" },
          },
        },
      },
    }),
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    host: "localhost",
    port: 8000,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:5000/api/",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
