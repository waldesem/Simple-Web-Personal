<script setup lang="ts">
import { shallowRef, watch, markRaw, defineAsyncComponent } from "vue";
import { useRoute } from "vue-router";

const DefaultLayout = defineAsyncComponent(
  () => import("@/components/layouts/DefaultLayout.vue"),
);

const route = useRoute();

const layout = shallowRef(DefaultLayout);

watch(
  () => route.meta.layout,
  async (metaLayout) => {
    if (metaLayout) {
      const component = await import(`@/components/layouts/${metaLayout}.vue`);
      layout.value = markRaw(component.default || DefaultLayout);
    }
  },
  { immediate: true },
);
</script>

<template>
  <UApp>
    <RouterView v-slot="{ Component }">
      <component :is="layout">
        <Transition mode="out-in" name="fade">
          <KeepAlive include="index" :max="1">
            <component :is="Component" />
          </KeepAlive>
        </Transition>
      </component>
    </RouterView>
  </UApp>
</template>
