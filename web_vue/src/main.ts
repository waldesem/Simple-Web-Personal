import { createApp } from "vue";
import ui from "@nuxt/ui/vue-plugin";
import App from "./App.vue";
import "./assets/main.css";
import { router } from "./router.ts";

createApp(App).use(router).use(ui).mount("#app");
