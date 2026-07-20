import { createApp } from "vue";
// import { addCollection } from "@iconify/vue";
import ui from "@nuxt/ui/vue-plugin";
import App from "./App.vue";
import "./assets/main.css";
import { api } from "./hooks";
import { router } from "./router";

// const { icons } = await import("@iconify-json/lucide");
// addCollection(icons);

const app = createApp(App);
app.use(router).use(ui);
app.provide("api", api);
app.mount("#app");
