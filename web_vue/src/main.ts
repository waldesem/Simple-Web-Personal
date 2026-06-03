import { createApp } from "vue";
import ui from "@nuxt/ui/vue-plugin";
import App from "./App.vue";
import "./assets/main.css";
import { api } from "@/plugins"
import { router } from "./router.ts";

const app = createApp(App)
app.use(router).use(ui).use(api)
app.mount("#app");
