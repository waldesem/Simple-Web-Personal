<script setup lang="ts">
import type { Work } from "@/types";
import { PropType } from "vue";

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
    {{ new Date(props.item.starts).toLocaleDateString() }}
  </LabelValue>
  <LabelValue v-if="props.item.finished" label="Окончание работы">
    {{ new Date(props.item.finished).toLocaleDateString() }}
  </LabelValue>
  <LabelValue label="Организация" :value="props.item.workplace" />
  <LabelValue
    v-if="props.item.address"
    label="Адрес"
    :value="props.item.address"
  />
  <LabelValue label="Должность" :value="props.item.position" />
  <LabelValue
    v-if="props.item.reason"
    label="Причина увольнения"
    :value="props.item.reason"
  />
</template>
