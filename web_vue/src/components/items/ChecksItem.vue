<script setup lang="ts">
import { PropType } from "vue";
import { conclusions, localDateStr } from "@/utils";
import type { ItemField, Verification } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Verification>,
    required: true,
  },
});

const fields = [
  { key: "workplace", label: "Место работы", value: props.item.workplace },
  { key: "document", label: "Документы", value: props.item.document },
  { key: "debt", label: "Задолженности", value: props.item.debt },
  { key: "bankruptcy", label: "Банкротство", value: props.item.bankruptcy },
  { key: "bki", label: "Проверка по БКИ", value: props.item.bki },
  { key: "courts", label: "Судебные решения", value: props.item.courts },
  {
    key: "affilation",
    label: "Аффилированность",
    value: props.item.affilation,
  },
  {
    key: "terrorist",
    label: "Проверка списка террористов",
    value: props.item.terrorist,
  },
  {
    key: "internet",
    label: "Проверка в открытых источниках",
    value: props.item.internet,
  },
  { key: "cronos", label: "Проверка Кронос", value: props.item.cronos },
  {
    key: "addition",
    label: "Дополнительная информация",
    value: props.item.addition,
  },
  { key: "comment", label: "Комментарии", value: props.item.comment },
  { key: "conclusion", label: "Заключение", slot: true },
  {
    key: "created",
    label: "Дата записи",
    value: localDateStr(props.item.created),
  },
] as ItemField[];
</script>

<template>
  <ItemCard :fields="fields">
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
