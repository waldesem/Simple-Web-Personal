<script setup lang="ts">
import { PropType } from "vue";
import type { Education, FormField } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Education>,
    default: () => ({}),
  },
});

const fields = [
  {
    element: "select",
    key: "view",
    label: "Вид образования",
    items: [
      "Основное общее",
      "Среднее общее",
      "Среднее профессиональное",
      "Высшее",
      "Неоконченное высшее образование",
      "Другое образование",
    ],
    attrs: { placeholder: "Выберите образование", required: true },
  },
  {
    element: "input",
    key: "institution",
    label: "Учебное заведение",
    attrs: { placeholder: "Учебное заведение", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "finished",
    label: "Год окончания",
    attrs: { placeholder: "Год окончания", pattern: "^\d{4}$" },
  },
  {
    element: "input",
    key: "specialty",
    attrs: { placeholder: "Специальность", maxlength: 255, required: true },
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
