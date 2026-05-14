<script setup lang="ts">
import { PropType } from "vue";
import type { FormField, Previous } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Previous>,
    default: () => ({}),
  },
});

const fields = [
  {
    element: "input",
    key: "surname",
    label: "Фамилия",
    attrs: { placeholder: "Фамилия", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "firstname",
    label: "Имя",
    attrs: { placeholder: "Имя", maxlength: 255 },
  },
  {
    element: "input",
    key: "patronymic",
    label: "Отчество",
    attrs: { placeholder: "Отчество", maxlength: 255 },
  },
  {
    element: "input",
    key: "changed",
    label: "Год изменения",
    attrs: { placeholder: "Год изменения", pattern: "^\d{4}$" },
  },
  {
    element: "textarea",
    key: "reason",
    label: "Причина",
    attrs: { placeholder: "Причина изменения", maxlength: 4096 },
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
