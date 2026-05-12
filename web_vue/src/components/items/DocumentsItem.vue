<script setup lang="ts">
import { computed, PropType } from "vue";
import { localStr } from "@/utils";
import type { ItemField, Passport } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Passport>,
    required: true,
  },
});

const fields = [
  { key: "view", label: "Вид документа" },
  { key: "series", label: "Серия документа" },
  { key: "digits", label: "Номер документа" },
  { key: "agency", label: "Кем выдан" },
  { key: "issue", label: "Дата выдачи" },
] as ItemField[];

const doc = computed(() => {
  return {
    ...props.item,
    issue: localStr(props.item.issue),
  };
});
</script>

<template>
  <ItemCard :fields="fields" :item="doc" />
</template>
