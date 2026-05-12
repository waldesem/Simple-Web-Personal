<script setup lang="ts">
import { PropType } from "vue";
import type { ItemField, Previous } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Previous>,
    required: true,
  },
});

const fields = [
  { key: "surname", label: "Фамилия", value: props.item.surname },
  { key: "firstname", label: "Имя", value: props.item.firstname },
  { key: "patronymic", label: "Отчество", value: props.item.patronymic },
  { key: "changed", label: "Год изменения", value: props.item.changed },
  { key: "reason", label: "Причина", value: props.item.reason },
] as ItemField[];
</script>

<template>
  <ItemCard :fields="fields" />
</template>
