<script setup lang="ts">
import { PropType } from "vue";
import type { FormField, Needs } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Needs>,
    default: () => ({}),
  },
});

const fields = [
  {
    element: "textarea",
    key: "info",
    label: "Информация",
    attrs: { placeholder: "Информация", maxlength: 4096, required: true },
  },
  {
    element: "input",
    key: "initiator",
    label: "Инициатор",
    attrs: { placeholder: "Инициатор", maxlength: 255, required: true },
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
