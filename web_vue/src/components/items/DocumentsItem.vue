<script setup lang="ts">
import { PropType } from "vue";
import { localDateStr } from "@/utils";
import type { ItemField, Passport } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Passport>,
    required: true,
  },
});

const fields = [
  { key: "view", label: "Вид документа", value: "Паспорт" },
  { key: "series", label: "Серия документа", value: props.item.series },
  { key: "digits", label: "Номер документа", value: props.item.digits },
  { key: "agency", label: "Кем выдан", value: props.item.agency },
  { key: "issue", label: "Дата выдачи", value: localDateStr(props.item.issue) },
] as ItemField[];
</script>

<template>
  <ItemCard :fields="fields" />
</template>
