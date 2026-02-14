import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import ui from "@nuxt/ui/vue-plugin";
import App from "./App.vue";
import './assets/main.css'

const app = createApp(App);

const router = createRouter({
  routes: [
    { path: "/", component: () => import("./pages/IndexView.vue") },
    { path: "/profile/:id", component: () => import("./pages/profile/ProfileView.vue") },
    { path: "/:catchAll(.*)", component: () => import("./pages/ErrorView.vue") },
  ],
  history: createWebHistory(),
});

app.use(router);
app.use(ui);

app.mount("#app");
