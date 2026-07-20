<script setup lang="ts">
import { shallowRef, watch, markRaw } from "vue";
import { useRoute } from "vue-router";
import UserLayout from "./components/layouts/UserLayout.vue";
import AdminLayout from "./components/layouts/AdminLayout.vue";

const route = useRoute();

const layout = shallowRef();

const layouts = {
  user: UserLayout,
  admin: AdminLayout,
};

watch(
  () => route.meta.layout,
  async (metaLayout) => {
    if (metaLayout) {
      layout.value = markRaw(layouts[metaLayout as keyof typeof layouts]);
    }
  },
  { immediate: true },
);
</script>

<template>
  <UApp>
    <UMain>
      <component v-if="layout" :is="layout" />
      <RouterView v-slot="{ Component }">
        <Transition mode="out-in" name="fade">
          <KeepAlive include="persons" :max="1">
            <component :is="Component" />
          </KeepAlive>
        </Transition>
      </RouterView>
      <UFooter v-once class="no-print" />
    </UMain>
  </UApp>
</template>
