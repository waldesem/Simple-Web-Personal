import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import ui from "@nuxt/ui/vue-plugin";
import App from "./App.vue";
import "./assets/main.css";

const router = createRouter({
  routes: [
    {
      name: "index",
      path: "/",
      redirect: "/home",
    },
    {
      name: "home",
      path: "/home",
      component: () => import("./components/pages/HomePage.vue"),
    },
    {
      name: "profile",
      path: "/profile/:id",
      props: true,
      component: () => import("./components/pages/ProfilePage.vue"),
    },
    {
      name: "users",
      path: "/users",
      component: () => import("./components/pages/UsersPage.vue"),
    },
    {
      path: "/:catchAll(.*)",
      redirect: "/home",
    },
  ],
  history: createWebHistory(),
});

createApp(App).use(router).use(ui).mount("#app");
