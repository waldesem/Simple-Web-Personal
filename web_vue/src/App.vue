<script setup lang="ts">
import { shallowRef, watch, markRaw } from "vue";
import { useRoute } from "vue-router";
import DefaultLayout from "@/components/layouts/DefaultLayout.vue";

const route = useRoute();

const layout = shallowRef(DefaultLayout);

watch(
  () => route.meta.layout,
  async (metaLayout) => {
    if (!metaLayout) {
      layout.value = DefaultLayout;
    } else {
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
          <KeepAlive include="HomePage" :max="1">
            <component :is="Component" />
          </KeepAlive>
        </Transition>
      </component>
    </RouterView>
  </UApp>
</template>
