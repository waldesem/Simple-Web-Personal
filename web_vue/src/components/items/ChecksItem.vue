<script setup lang="ts">
import { computed, PropType } from "vue";
import { conclusions, localDateStr } from "@/utils";
import type { ItemField, Verification } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Verification>,
    required: true,
  },
});

const fields = [
  { key: "workplace", label: "Место работы" },
  { key: "document", label: "Документы" },
  { key: "debt", label: "Задолженности" },
  { key: "bankruptcy", label: "Банкротство" },
  { key: "bki", label: "Проверка по БКИ" },
  { key: "courts", label: "Судебные решения" },
  { key: "affilation", label: "Аффилированность" },
  { key: "terrorist", label: "Проверка списка террористов" },
  { key: "internet", label: "Проверка в открытых источниках" },
  { key: "cronos", label: "Проверка Кронос" },
  { key: "addition", label: "Дополнительная информация" },
  { key: "comment", label: "Комментарии" },
  { key: "conclusion", label: "Заключение", slot: true },
  { key: "created", label: "Дата записи" },
] as ItemField[];

const check = computed(() => {
  return {
    ...props.item,
    created: localDateStr(props.item.created),
  };
});
</script>

<template>
  <ItemCard :fields="fields" :item="check">
    <template #conclusion v-if="props.item.conclusion">
      <UBadge
        :color="
          props.item.conclusion === conclusions.agreed
            ? 'success'
            : props.item.conclusion === conclusions.comments
              ? 'warning'
              : props.item.conclusion === conclusions.cancel
                ? 'neutral'
                : 'error'
        "
        :label="props.item.conclusion"
      />
    </template>
  </ItemCard>
</template>
