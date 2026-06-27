<script setup lang="ts">
import { shallowRef, watch, markRaw, defineAsyncComponent } from "vue";
import { useRoute } from "vue-router";

const DefaultLayout = defineAsyncComponent(
  () => import("@/components/layouts/DefaultLayout.vue"),
);

const route = useRoute();

const Layout = shallowRef(DefaultLayout);

watch(
  () => route.meta.layout,
  async (metaLayout) => {
    if (!metaLayout) Layout.value = DefaultLayout;
    else {
      const component = await import(`@/components/layouts/${metaLayout}.vue`);
      Layout.value = markRaw(component.default);
    }
  },
  { immediate: true },
);
</script>

<template>
  <UApp>
    <RouterView v-slot="{ Component }">
      <component :is="Layout">
        <Transition mode="out-in" name="fade">
          <KeepAlive include="persons" :max="1">
            <component :is="Component" />
          </KeepAlive>
        </Transition>
      </component>
    </RouterView>
  </UApp>
</template>
