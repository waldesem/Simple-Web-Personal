<script setup lang="ts">
import { PropType } from "vue";
import { localStr } from "@/utils";
import type { Needs } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Needs>,
    required: true,
  },
});
</script>

<template>
  <LabelValue label="Информация" :value="props.item.info" />
  <LabelValue label="Иннициатор" :value="props.item.initiator" />
  <LabelValue label="Дата записи">
    {{ localStr(props.item.created) }}
  </LabelValue>
</template>
