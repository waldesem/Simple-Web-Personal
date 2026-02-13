<script setup lang="ts">
import type { Passport } from "@/types";
import { PropType } from "vue";

const props = defineProps({
  item: {
    type: Object as PropType<Passport>,
    required: true,
  },
});
</script>

<template>
  <LabelValue label="Вид документа" :value="props.item.view" />
  <LabelValue label="Серия документа" :value="props.item.series" />
  <LabelValue label="Номер документа" :value="props.item.digits" />
  <LabelValue label="Кем выдан" :value="props.item.agency" />
  <LabelValue label="Дата выдачи">
    {{ new Date(props.item.issue).toLocaleDateString() }}
  </LabelValue>
</template>
