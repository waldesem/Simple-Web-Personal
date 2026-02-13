<script setup lang="ts">
import type { Needs } from "@/types";
import { PropType } from "vue";

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
    {{ new Date(props.item.created).toLocaleDateString() }}
  </LabelValue>
</template>
