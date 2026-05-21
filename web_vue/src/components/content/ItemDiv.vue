<script setup lang="ts">
import type { PropType } from "vue";
import type { ItemFields, Items } from "@/types";

const props = defineProps({
  fields: {
    type: Array as PropType<ItemFields<Items[keyof Items]>[]>,
    required: true,
  },
  item: {
    type: Object as PropType<Items[keyof Items]>,
    default: () => ({}),
  },
});
</script>

<template>
  <div v-for="field in fields" :key="field.key" class="m-2">
    <div v-if="item[field.key]" class="flex grid grid-cols-12 gap-3 mb-4">
      <div class="col-span-3">
        {{ field.label }}
      </div>
      <div class="col-span-9 wrap-break-word"">
        <component v-if="field.component" :is="field.component(item)" />
        <slot v-else-if="field.slot" :name="field.key" />
        <span v-else>{{ field.div ? field.div(item) : item[field.key] }}</span>
      </div>
    </div>
  </div>
</template>
