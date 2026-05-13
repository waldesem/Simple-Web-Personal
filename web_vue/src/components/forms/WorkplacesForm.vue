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

const parser = fallbackParser(schemaWork)
const form = computed(() => parser(props.item));

const fields = [
  {
    element: "input",
    key: "starts",
    label: "Начало работы",
    type: "date",
    required: true,
  },
  {
    element: "input",
    key: "finished",
    label: "Окончание работы",
    type: "date",
    required: true,
  },
  {
    element: "input",
    key: "workplace",
    label: "Место работы",
    required: true,
  },
  {
    element: "input",
    key: "position",
    label: "Должность",
    required: true,
  },
  {
    element: "input",
    key: "address",
    label: "Адрес организации",
  },
  {
    element: "textarea",
    key: "reason",
    label: "Причина увольнения",
  },
] as FormField[];
</script>

<template>
  <FormCard
    :fields="fields"
    :item="form"
    :schema="schemaWork"
    @submit="emit('update', $event)"
  />
</template>
