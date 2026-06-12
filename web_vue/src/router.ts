import { createRouter, createWebHistory } from "vue-router";

export const router = createRouter({
  routes: [
    {
      name: "home",
      path: "/",
      component: () => import("./components/pages/HomePage.vue"),
      meta: { layout: "LayoutView" },
    },
    {
      name: "profile",
      path: "/profile/:id",
      props: true,
      component: () => import("./components/pages/ProfilePage.vue"),
      meta: { layout: "LayoutView" },
    },
    {
      name: "users",
      path: "/users",
      component: () => import("./components/pages/UsersPage.vue"),
      meta: { layout: "LayoutView" },
    },
    {
      path: "/:catchAll(.*)",
      redirect: "/",
    },
  ],
  history: createWebHistory(),
});
