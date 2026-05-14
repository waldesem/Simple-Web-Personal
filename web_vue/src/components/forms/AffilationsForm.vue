<script setup lang="ts">
import { PropType } from "vue";
import type { Affilation, FormField } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Affilation>,
    default: () => ({}),
  },
});

const fields = [
  {
    element: "input",
    key: "view",
    label: "Вид участия",
    attrs: { placeholder: "Вид участия", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "organization",
    label: "Организация",
    attrs: { placeholder: "Организация", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "inn",
    label: "ИНН",
    attrs: { placeholder: "Организация", pattern: "^\d{10,12}$" },
  },
  {
    element: "textarea",
    key: "activity",
    label: "Деятельность",
    attrs: { placeholder: "Деятельность", maxlength: 4096 },
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
