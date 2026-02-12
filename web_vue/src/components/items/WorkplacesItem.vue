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
  <ElementLabelValue
    label="Текущая работа"
    :value="props.item.finished ? 'Нет' : 'Да'"
  />
  <ElementLabelValue label="Начало работы">
    {{ new Date(props.item.starts).toLocaleDateString() }}
  </ElementLabelValue>
  <ElementLabelValue v-if="props.item.finished" label="Окончание работы">
    {{ new Date(props.item.finished).toLocaleDateString() }}
  </ElementLabelValue>
  <ElementLabelValue label="Место" :value="props.item.workplace" />
  <ElementLabelValue label="Адрес" :value="props.item.address" />
  <ElementLabelValue label="Должность" :value="props.item.position" />
  <ElementLabelValue label="Причина увольнения" :value="props.item.reason" />
</template>
