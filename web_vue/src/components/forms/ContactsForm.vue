<script setup lang="ts">
import { PropType } from "vue";
import type { Contact, FormField } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Contact>,
    default: () => ({}),
  },
});

const fields = [
  {
    element: "select",
    key: "view",
    label: "Вид контакта",
    items: ["Телефон", "Электронная почта", "Другое"],
    required: true,
  },
  {
    element: "input",
    key: "contact",
    label: "Контакт",
    required: true,
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
