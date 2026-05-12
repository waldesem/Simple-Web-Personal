<script setup lang="ts">
import { computed, PropType } from "vue";
import { decisions, localStr } from "@/utils";
import type { ItemField, Pfo } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Pfo>,
    required: true,
  },
});

const fields = [
  { key: "theme", label: "Тема проверки" },
  { key: "results", label: "Результаты" },
  { key: "conclusion", label: "Заключение", slot: true },
  { key: "created", label: "Дата записи" },
] as ItemField[];

const pfo = computed(() => {
  return {
    ...props.item,
    created: localStr(props.item.created),
  };
});

const color = computed(() => {
  switch (props.item.conclusion) {
    case decisions.agreed:
      return "success";
    case decisions.comments:
      return "warning";
    case decisions.cancel:
      return "neutral";
    default:
      return "error";
  }
});
</script>

<template>
  <ItemCard :fields="fields" :item="pfo">
    <template #conclusion>
      <UBadge :color="color" :label="props.item.conclusion" />
    </template>
  </ItemCard>
</template>
