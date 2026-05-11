<script setup lang="ts">
import { PropType } from "vue";
import { schemaDoc } from "@/schema";
import type { FormField, Passport } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Passport>,
    default: () => ({}),
  },
});

const form = {
  id: props.item.id ?? null,
  view: props.item.view || "",
  series: props.item.series || "",
  digits: props.item.digits || "",
  agency: props.item.agency || "",
  issue: props.item.issue || "",
};
const fields = [
  {
    element: "select",
    key: "view",
    label: "Вид документа",
    items: ["Паспорт", "Иностранный паспорт", "Другое"],
    required: true,
  },
  {
    element: "input",
    key: "series",
    label: "Серия",
    maxlength: 12,
  },
  {
    element: "input",
    key: "digits",
    label: "Номер",
    maxlength: 12,
    required: true,
  },
  {
    element: "input",
    key: "agency",
    label: "Кем выдан",
  },
  {
    element: "input",
    key: "issue",
    label: "Дата выдачи",
    type: "date",
    required: true,
  },
] as FormField[];
</script>

<template>
  <FormCard
    :fields="fields"
    :item="form"
    :schema="schemaDoc"
    @submit="emit('update', $event)"
  />
</template>
