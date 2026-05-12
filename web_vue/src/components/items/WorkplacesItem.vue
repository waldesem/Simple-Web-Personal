<script setup lang="ts">
import { computed, PropType } from "vue";
import { localDateStr } from "@/utils";
import type { ItemField, Work } from "@/types";
import ItemCard from "../element/ItemCard.vue";

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    required: true,
  },
});

const work = computed(() => {
  return {
    ...props.item,
    nowWork: props.item.finished ? "Нет" : "Да",
    starts: localDateStr(props.item.starts),
    finished: localDateStr(props.item.finished),
  };
});

const fields = [
  { key: "nowWork", label: "Текущая работа", value: work.value.nowWork },
  { key: "starts", label: "Начало работы", value: work.value.starts },
  { key: "finished", label: "Дата увольнения", value: work.value.finished },
  { key: "workplace", label: "Организация", value: work.value.workplace },
  { key: "address", label: "Организация", value: work.value.address },
  { key: "position", label: "Должность", value: work.value.position },
  { key: "reason", label: "Причина увольнения", value: work.value.reason },
] as ItemField[];
</script>

<template>
  <ItemCard :fields="fields" />
</template>
