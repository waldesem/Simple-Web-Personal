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
    element: "select",
    key: "view",
    label: "Вид участия",
    items: [
      "Являлся государственным/муниципальным служащим",
      "Участвует в деятельности коммерческих организаций",
    ],
    required: true,
  },
  {
    element: "input",
    key: "organization",
    label: "Организация",
    required: true,
  },
  {
    element: "input",
    key: "inn",
    label: "ИНН",
    pattern: "^\d{10,12}$",
  },
  {
    element: "textarea",
    key: "activity",
    label: "Деятельность",
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
