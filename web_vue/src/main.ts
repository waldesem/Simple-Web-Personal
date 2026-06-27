import { createApp } from "vue";
import { handleHotUpdate } from "vue-router/auto-routes";
import { addCollection } from "@iconify/vue";
import ui from "@nuxt/ui/vue-plugin";
import App from "./App.vue";
import "./assets/main.css";
import { api } from "./hooks";
import { router } from "./router";

if (import.meta.hot) {
  handleHotUpdate(router);
}

const { icons } = await import("@iconify-json/mono-icons");
addCollection(icons);

const app = createApp(App);
app.use(router).use(ui);
app.provide("api", api);
app.mount("#app");
