<script setup lang="ts">
import { PropType } from "vue";
import type { Address, FormField } from "@/types";

const emit = defineEmits(["update"]);

const props = defineProps({
  item: {
    type: Object as PropType<Address>,
    default: () => ({}),
  },
});

const fields = [
  {
    element: "select",
    key: "view",
    label: "Вид адреса",
    items: ["Адрес регистрации", "Адрес проживания", "Другое"],
    attrs: { placeholder: "Выберите адрес", required: true },
  },
  {
    element: "textarea",
    key: "address",
    label: "Адрес",
    attrs: { placeholder: "Введите адрес", maxlength: 4096, required: true },
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
