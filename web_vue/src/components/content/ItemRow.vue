<script setup lang="ts">
import { type PropType } from "vue";
import type { person as personFields, itemsFields } from "@/schema/items";
import { Items, Person } from "@/types";

const props = defineProps({
  data: {
    type: Object as PropType<Person | Items[keyof Items]>,
    required: true,
  },
  field: {
    type: Object as PropType<
      | (typeof personFields)[number]
      | (typeof itemsFields)[keyof typeof itemsFields][number]
    >,
    required: true,
  },
});
</script>

<template>
  <div class="grid grid-cols-12 gap-4 mb-4">
    <div class="col-span-3">{{ props.field.label }}</div>
    <div class="col-span-9 wrap-break-word">
      <component
        v-if="field.component"
        :is="field.component(props.data as any)"
      />
      <slot v-else-if="field.slot" :name="field.key" />
      <span v-else>
        {{
          props.field.foo
            ? props.field.foo(props.data as any)
            : props.data[props.field.key as keyof typeof props.data]
        }}
      </span>
    </div>
  </div>
</template>
