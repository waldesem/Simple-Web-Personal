<script setup lang="ts">
import { type PropType } from "vue";
import { ItemField, Items } from "@/types";

const props = defineProps({
  fields: {
    type: Array as PropType<ItemField<Items[keyof Items][]>[]>,
    required: true,
  },
  item: {
    type: Object as PropType<Items[keyof Items][number]>,
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
        <component :is="field.component(item)" />
      </div>

      <div v-else-if="field.div" class="col-span-9 wrap-break-word">
        {{ field.div(item) }}
      </div>

      <div v-else class="col-span-9 wrap-break-word">
        {{ item[field.key] }}
      </div>
    </div>
  </div>
</template>
