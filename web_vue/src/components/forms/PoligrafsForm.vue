<script setup lang="ts">
import { PropType } from "vue";
import { decisions } from "@/utils";
import type { FormField, Pfo } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Pfo>,
    default: () => ({}),
  },
});

const fields = [
  {
    element: "select",
    key: "theme",
    label: "Тема проверки",
    items: [
      "Проверка кандидата",
      "Служебная проверка",
      "Служебное расследование",
      "Плановое мероприятие",
    ],
    attrs: { placeholder: "Выберите тему", required: true },
  },
  {
    element: "textarea",
    key: "results",
    label: "Результат",
    attrs: { placeholder: "Результат", maxlength: 4096, required: true },
  },
  {
    element: "select",
    key: "conclusion",
    label: "Результат",
    items: Object.values(decisions),
    attrs: { placeholder: "Выберите результат", required: true },
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
