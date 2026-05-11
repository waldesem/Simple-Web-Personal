<script setup lang="ts">
import { PropType } from "vue";
import type { FormField, Staff } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Staff>,
    default: () => ({}),
  },
});

const fields = [
  {
    element: "input",
    key: "position",
    label: "Должность",
    required: true,
  },
  {
    element: "input",
    key: "department",
    label: "Подразделение",
  },
] as FormField[];
</script>

<template>
  <FormCard
    :fields="fields"
    :item="props.item"
    @submit="emit('update', $event)"
  />
</template>
