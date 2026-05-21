import { createApp, onMounted } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import ui from "@nuxt/ui/vue-plugin";
import App from "./App.vue";
import "./assets/main.css";

export default {
  setup() {
    onMounted(() => {
      import("./plugins/iconify-local");
    });
  },
};

const router = createRouter({
  routes: [
    {
      name: "home",
      path: "/",
      component: () => import("./components/pages/HomePage.vue"),
    },
    {
      name: "profile",
      path: "/profile/:id",
      component: () => import("./components/pages/ProfilePage.vue"),
    },
    {
      path: "/:catchAll(.*)",
      redirect: "/",
    },
  ],
  history: createWebHistory(),
});

createApp(App).use(router).use(ui).mount("#app");
