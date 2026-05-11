<script setup lang="ts">
import { computed, PropType } from "vue";
import { localDateStr } from "@/utils";
import type { Inquisition, ItemField } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    required: true,
  },
});

const fields = [
  { key: "theme", label: "Тема проверки" },
  { key: "info", label: "Информация" },
  { key: "created", label: "Дата записи" },
] as ItemField[];

const investigation = computed(() => {
  return {
    ...props.item,
    created: localDateStr(props.item.created),
  };
});
</script>

<template>
  <ItemCard :fields="fields" :item="investigation" />
</template>
