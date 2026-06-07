import { createApp } from "vue";
import { router } from "./router.ts";
import { addCollection } from "@iconify/vue";
import ui from "@nuxt/ui/vue-plugin";
import App from "./App.vue";
import { api } from "@/api";
import "./assets/main.css";

const { icons } = await import("@iconify-json/mono-icons");
addCollection(icons);

const app = createApp(App);
app.use(router).use(ui).provide("api", api);
app.mount("#app");
