<script setup lang="ts">
import { computed, PropType } from "vue";
import { fallbackParser, schemaDoc } from "@/schema";
import type { FormField, Passport } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Passport>,
    default: () => ({}),
  },
});

const fallback = computed(() => fallbackParser(schemaDoc, props.item));

const fields = [
  {
    element: "select",
    key: "view",
    label: "Вид документа",
    items: ["Паспорт", "Иностранный паспорт", "Другое"],
    attrs: { placeholder: "Выберите документ", required: true },
  },
  {
    element: "input",
    key: "series",
    label: "Серия",
    attrs: { placeholder: "Серия", maxlength: 16 },
  },
  {
    element: "input",
    key: "digits",
    label: "Номер",
    attrs: { placeholder: "Номер", maxlength: 16, required: true },
  },
  {
    element: "input",
    key: "agency",
    label: "Кем выдан",
    attrs: { placeholder: "Орган выдавший", maxlength: 255 },
  },
  {
    element: "input",
    key: "issue",
    label: "Дата выдачи",
    attrs: { type: "date", required: true },
  },
] as FormField[];
</script>

<template>
  <FormCard
    :fields="fields"
    :item="fallback"
    :schema="schemaDoc"
    @submit="emit('update', $event)"
  />
</template>
