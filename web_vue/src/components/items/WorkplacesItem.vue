<script setup lang="ts">
import { computed, PropType } from "vue";
import { localStr } from "@/utils";
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
    starts: localStr(props.item.starts),
    finished: localStr(props.item.finished),
  };
});

const fields = [
  { key: "nowWork", label: "Текущая работа" },
  { key: "starts", label: "Начало работы" },
  { key: "finished", label: "Дата увольнения" },
  { key: "workplace", label: "Организация" },
  { key: "address", label: "Организация" },
  { key: "position", label: "Должность" },
  { key: "reason", label: "Причина увольнения" },
] as ItemField[];
</script>

<template>
  <ItemCard :fields="fields" :item="work" />
</template>
