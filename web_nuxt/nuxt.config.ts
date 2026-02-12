import { fileURLToPath } from "url";

export default defineNuxtConfig({
  alias: {
    "@/": fileURLToPath(new URL("./src/app", import.meta.url)),
  },
  app: {
    keepalive: { include: "index" },
    pageTransition: { name: "page", mode: "out-in" },
    head: {
      title: "StaffSec - кадровая безопасность",
    },
  },
  build: {
    analyze: {
      analyzerMode: "static",
    },
  },
  compatibilityDate: "2026-01-30",
  css: ["~/assets/css/main.css"],
  experimental: {
    entryImportMap: false,
  },
  icon: {
    clientBundle: {
      scan: true,
    },
  },
  modules: ["@nuxt/ui", "@nuxt/eslint", "@vueuse/nuxt"],
  nitro: {
    output: {
      publicDir: "../server_flask/app/static",
    },
    prerender: {
      crawlLinks: true,
      routes: ["/"],
    },
  },
  routeRules: {
    "/routes/**": { proxy: "http://127.0.0.1:5000/routes/**" },
  },
  spaLoadingTemplate: true,
  ssr: false,
  ui: {
    fonts: false,
  },
  vite: {
    build: {
      emptyOutDir: true,
    },
  },
});
