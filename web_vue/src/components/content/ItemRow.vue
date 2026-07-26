<script setup lang="ts">
import type { PropType } from "vue";
import type { ItemType, FieldsType } from "./ItemDiv.vue";

const { data, field } = defineProps({
  data: {
    type: Object as PropType<ItemType>,
    required: true,
  },
  field: {
    type: Object as PropType<FieldsType[number]>,
    required: true,
  },
});
</script>

<template>
  <div class="grid grid-cols-12 gap-4 mb-4">
    <div class="col-span-3">{{ field.label }}</div>
    <div class="col-span-9 wrap-break-word">
      <slot v-if="field.slot" />
      <component
        v-else-if="field.component"
        :is="field.component(data as any)"
      />
      <span v-else>
        {{
          field.foo
            ? field.foo(data as any)
            : data[field.key as keyof typeof data]
        }}
      </span>
    </div>
  </div>
</template>
