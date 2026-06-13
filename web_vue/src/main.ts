import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import { routes, handleHotUpdate } from "vue-router/auto-routes";
import { addCollection } from "@iconify/vue";
import ui from "@nuxt/ui/vue-plugin";
import App from "./App.vue";
import "./assets/main.css";

const router = createRouter({
  history: createWebHistory(),
  routes,
});

if (import.meta.hot) {
  handleHotUpdate(router);
}

const { icons } = await import("@iconify-json/mono-icons");
addCollection(icons);

const app = createApp(App);
app.use(router).use(ui);
app.mount("#app");
