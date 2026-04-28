import { createApp, onMounted } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import ui from "@nuxt/ui/vue-plugin";
import App from "./App.vue";
import "./assets/main.css";

export default {
  setup() {
    onMounted(() => {
      // Загрузится только после рендера основного приложения
      import("./plugins/iconify-local");
    });
  },
};

const router = createRouter({
  routes: [
    {
      name: "index",
      path: "/",
      component: () => import("./pages/IndexView.vue"),
    },
    {
      name: "profile",
      path: "/profile/:id",
      component: () => import("./pages/ProfileView.vue"),
    },
    {
      path: "/:catchAll(.*)",
      redirect: "/",
    },
  ],
  history: createWebHistory(),
});

const app = createApp(App).use(router).use(ui);

app.mount("#app");
