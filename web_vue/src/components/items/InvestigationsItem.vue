<script setup lang="ts">
import { PropType } from "vue";
import { localDateStr } from "@/utils";
import type { Inquisition, ItemField } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    required: true,
  },
});

const fields = [
  { key: "theme", label: "Тема проверки", value: props.item.theme },
  { key: "info", label: "Информация", value: props.item.info },
  {
    key: "created",
    label: "Дата записи",
    value: localDateStr(props.item.created),
  },
] as ItemField[];
</script>

<template>
  <ItemCard :fields="fields" />
</template>
