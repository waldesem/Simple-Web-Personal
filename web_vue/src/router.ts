import { createRouter, createWebHistory } from "vue-router";
import { handleHotUpdate } from "vue-router/auto-routes";
import { routes } from "vue-router/auto-routes";

export const router = createRouter({
  history: createWebHistory(),
  routes,
});

if (import.meta.hot) {
  handleHotUpdate(router);
}
