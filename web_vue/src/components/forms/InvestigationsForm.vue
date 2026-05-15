<script setup lang="ts">
import { PropType } from "vue";
import type { FormField, Inquisition } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    default: () => ({}),
  },
  fields: {
    type: Array as PropType<FormField[]>,
    required: true,
  },
});
</script>

<template>
  <FormCard
    :fields="props.fields"
    :item="props.item"
    @submit="emit('update', $event)"
  />
</template>
