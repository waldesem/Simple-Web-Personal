<script setup lang="ts">
import { PropType } from "vue";
import { localDateStr } from "@/utils";
import type { Work } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    required: true,
  },
});
</script>

<template>
  <LabelValue
    label="Текущая работа"
    :value="props.item.finished ? 'Нет' : 'Да'"
  />
  <LabelValue label="Начало работы" :value="localDateStr(props.item.starts)" />
  <LabelValue
    label="Окончание работы"
    :value="localDateStr(props.item.finished)"
  />
  <LabelValue label="Организация" :value="props.item.workplace" />
  <LabelValue label="Адрес" :value="props.item.address" />
  <LabelValue label="Должность" :value="props.item.position" />
  <LabelValue label="Причина увольнения" :value="props.item.reason" />
</template>
