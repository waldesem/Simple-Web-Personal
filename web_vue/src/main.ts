import { createApp } from "vue";
import { router } from "./router.ts";
import { addCollection } from "@iconify/vue";
import { icons } from "@iconify-json/mono-icons";
import ui from "@nuxt/ui/vue-plugin";
// import { api } from "@/plugins";
import App from "./App.vue";
import "./assets/main.css";

addCollection(icons);

const app = createApp(App);
app.use(router).use(ui); //.use(api);
app.mount("#app");
