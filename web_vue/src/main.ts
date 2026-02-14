import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import ui from "@nuxt/ui/vue-plugin";
import App from "./App.vue";
import IndexView from "./pages/IndexView.vue";
import ErrorView from "./pages/ErrorView.vue";
import ProfileView from "./pages/profile/ProfileView.vue";
import './assets/main.css'

const app = createApp(App);

const router = createRouter({
  routes: [
    { path: "/", component: IndexView },
    { path: "/profile/:id", component: ProfileView },
    { path: "/:catchAll(.*)", component: ErrorView },
  ],
  history: createWebHistory(),
});

app.use(router);
app.use(ui);

app.mount("#app");
