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
    required: true,
  },
  {
    element: "input",
    key: "firstname",
    label: "Имя",
  },
  {
    element: "input",
    key: "patronymic",
    label: "Отчество",
  },
  {
    element: "input",
    key: "changed",
    label: "Год изменения",
    pattern: "^\d{4}$",
  },
  {
    element: "textarea",
    key: "reason",
    label: "Причина",
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
