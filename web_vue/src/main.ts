import { createApp } from "vue";
import ui from "@nuxt/ui/vue-plugin";
import App from "./App.vue";
import { api } from "./hooks";
import { router } from "./router";
import "./assets/main.css";

const app = createApp(App);

app.use(router).use(ui).provide("api", api).mount("#app");
