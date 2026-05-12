<script setup lang="ts">
import { PropType } from "vue";
import type { Affilation, ItemField } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Affilation>,
    required: true,
  },
});

const fields = [
  { key: "view", label: "Тип участия", value: props.item.view },
  { key: "organization", label: "Организация", value: props.item.organization },
  { key: "inn", label: "ИНН", value: props.item.inn },
  { key: "activity", label: "Деятельность", value: props.item.activity },
] as ItemField[];
</script>

<template>
  <ItemCard :fields="fields" />
</template>
