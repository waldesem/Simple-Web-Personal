<script setup lang="ts">
import { PropType } from "vue";
import type { Work } from "@/types";
import { localStr } from "@/utils";

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
  <LabelValue label="Начало работы">
    {{ localStr(props.item.starts) }}
  </LabelValue>
  <LabelValue label="Окончание работы">
    {{ localStr(props.item.finished) }}
  </LabelValue>
  <LabelValue label="Организация" :value="props.item.workplace" />
  <LabelValue label="Адрес" :value="props.item.address" />
  <LabelValue label="Должность" :value="props.item.position" />
  <LabelValue label="Причина увольнения" :value="props.item.reason" />
</template>
