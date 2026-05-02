<script setup lang="ts">
import { PropType } from "vue";
import { localDateStr } from "@/utils";
import type { Passport } from "@/types";

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
  <LabelValue label="Дата выдачи" :value="localDateStr(props.item.issue)" />
</template>
