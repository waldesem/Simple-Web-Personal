<script setup lang="ts">
import { type PropType } from "vue";
import type { ItemField } from "@/types";

const props = defineProps({
  fields: {
    type: Object as PropType<ItemField[]>,
    required: true,
  },
  item: {
    type: Object,
    default: () => ({}),
  },
});
</script>

<template>
  <div v-for="field in fields" :key="field.key">
    <div v-if="item[field.key]" class="flex grid grid-cols-12 gap-3 mb-4">
      <div class="col-span-3">
        {{ field.label }}
      </div>
      <div v-if="field.slot" class="col-span-9">
        <slot :name="field.key" />
      </div>
      <div v-else-if="field.component" class="col-span-9">
        <component :is="field.component(item[field.key])" />
      </div>
      <div v-else class="col-span-9 wrap-break-word">
        {{ field.div ? field.div(item[field.key]) : item[field.key] }}
      </div>
    </div>
  </div>
</template>
