import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import ui from "@nuxt/ui/vite";
import path from "path";

export default defineConfig({
  build: {
    emptyOutDir: true,
    outDir: "../server_flask/app/static",
  },
  plugins: [
    vue(),
    ui({
      prefix: "NU",
      ui: {
        colors: {
          primary: "blue",
          neutral: "gray",
        },
        icons: {
          arrowDown: "i-mi-arrow-down",
          arrowLeft: "i-mi-arrow-left",
          arrowRight: "i-mi-arrow-right",
          arrowUp: "i-mi-arrow-up",
          caution: "i-mi-circle-warning",
          check: "i-mi-check",
          chevronDoubleLeft: "i-mi-chevrons-left",
          chevronDoubleRight: "i-mi-chevrons-right",
          chevronDown: "i-mi-chevron-down",
          chevronLeft: "i-mi-chevron-left",
          chevronRight: "i-mi-chevron-right",
          chevronUp: "i-mi-chevron-up",
          close: "i-mi-close",
          copy: "i-mi-clipboard",
          copyCheck: "i-mi-clipboard-check",
          dark: "i-mi-moon",
          drag: "i-mi-drag",
          ellipsis: "i-mi-options-horizontal",
          error: "i-mi-circle-error",
          external: "i-mi-arrow-right-up",
          eye: "i-mi-eye",
          eyeOff: "i-mi-eye-off",
          file: "i-mi-document-empty",
          folder: "i-mi-folder",
          folderOpen: "i-mi-folder-add",
          hash: "i-mi-comment",
          info: "i-mi-circle-information",
          light: "i-mi-sun",
          loading: "i-mi-refresh",
          menu: "i-mi-menu",
          minus: "i-mi-remove",
          panelClose: "i-mi-two-columns",
          panelOpen: "i-mi-two-rows",
          plus: "i-mi-add",
          reload: "i-mi-refresh",
          search: "i-mi-search",
          stop: "i-mi-stop",
          success: "i-mi-circle-check",
          system: "i-mi-computer",
          tip: "i-mi-notification",
          upload: "i-mi-export",
          warning: "i-mi-warning",
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
            header: "p-3",
            content: "sm:max-w-xl",
          },
        },
        pageBody: {
          base: "pb-4 my-4 space-y-4",
        },
        pageHeader: {
          slots: {
            root: "relative border-none pt-20 pb-4",
            title: "text-2xl sm:text-3xl text-red-800",
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
      "@": path.resolve(__dirname, "src"),
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
