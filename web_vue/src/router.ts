import { createRouter, createWebHistory } from "vue-router";

export const router = createRouter({
  routes: [
    {
      name: "home",
      path: "/",
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
      redirect: "/",
    },
  ],
  history: createWebHistory(),
});
