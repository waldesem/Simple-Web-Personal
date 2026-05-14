<script setup lang="ts">
import { computed, PropType } from "vue";
import { fallbackParser, schemaWork } from "@/schema";
import type { FormField, Work } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    default: () => ({}),
  },
});

const fallback = computed(() => fallbackParser(schemaWork, props.item));

const fields = [
  {
    element: "input",
    key: "starts",
    label: "Начало работы",
    attrs: { type: "date", required: true },
  },
  {
    element: "input",
    key: "finished",
    label: "Окончание работы",
    attrs: { type: "date" },
  },
  {
    element: "input",
    key: "workplace",
    label: "Место работы",
    attrs: { placeholder: "Место работы", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "position",
    label: "Должность",
    attrs: { placeholder: "Должность", maxlength: 255, required: true },
  },
  {
    element: "input",
    key: "address",
    label: "Адрес организации",
    attrs: { placeholder: "Адрес организации", maxlength: 255 },
  },
  {
    element: "textarea",
    key: "reason",
    label: "Причина увольнения",
    attrs: { placeholder: "Причина увольнения", maxlength: 4096 },
  },
] as FormField[];
</script>

<template>
  <FormCard
    :fields="fields"
    :item="fallback"
    :schema="schemaWork"
    @submit="emit('update', $event)"
  />
</template>
