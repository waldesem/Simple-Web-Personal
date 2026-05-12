<script setup lang="ts">
import { PropType } from "vue";
import { localDateStr } from "@/utils";
import type { ItemField, Needs } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Needs>,
    required: true,
  },
});

const fields = [
  { key: "info", label: "Информация", value: props.item.info },
  { key: "initiator", label: "Инициатор", value: props.item.initiator },
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
