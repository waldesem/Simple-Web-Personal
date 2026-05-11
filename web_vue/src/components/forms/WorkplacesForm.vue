<script setup lang="ts">
import { PropType } from "vue";
import { schemaWork } from "@/schema";
import type { FormField, Work } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    default: () => ({}),
  },
});

const form = {
  id: props.item.id ?? null,
  starts: props.item.starts || "",
  finished: props.item.finished || "",
  workplace: props.item.workplace || "",
  position: props.item.position || "",
  address: props.item.address || "",
  reason: props.item.reason || "",
};

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
