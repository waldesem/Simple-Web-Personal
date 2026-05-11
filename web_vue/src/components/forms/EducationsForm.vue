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
    required: true,
  },
  {
    element: "input",
    key: "institution",
    label: "Учебное заведение",
    required: true,
  },
  {
    element: "input",
    key: "finished",
    label: "Год окончания",
    pattern: "^\d{4}$",
    required: true,
  },
  {
    element: "input",
    key: "specialty",
    label: "Специальность",
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
