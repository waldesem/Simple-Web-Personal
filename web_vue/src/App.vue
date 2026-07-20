<script setup lang="ts">
import { shallowRef, watch, markRaw } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

const layout = shallowRef(null);

watch(
  () => route.meta.layout,
  async (metaLayout) => {
    if (metaLayout) {
      const component = await import(`@/components/layouts/${metaLayout}.vue`);
      layout.value = markRaw(component.default);
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
