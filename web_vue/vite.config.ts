import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import ui from "@nuxt/ui/vite";

export default defineConfig({
  plugins: [
    vue(),
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
});
