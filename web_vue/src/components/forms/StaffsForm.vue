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
    attrs: { placeholder: "Должность", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "department",
    label: "Подразделение",
    attrs: { placeholder: "Подразделение", maxlength: 255 },
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
