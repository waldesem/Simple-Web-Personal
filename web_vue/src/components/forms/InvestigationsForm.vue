<script setup lang="ts">
import { PropType } from "vue";
import type { FormField, Inquisition } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    default: () => ({}),
  },
});

const fields = [
  {
    element: "input",
    key: "theme",
    label: "Тема проверки",
    attrs: { placeholder: "Тема проверки", maxlength: 255, required: true },
  },
  {
    element: "textarea",
    key: "info",
    label: "Информация",
    attrs: { placeholder: "Информация", maxlength: 4096, required: true },
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
