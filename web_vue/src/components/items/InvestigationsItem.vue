<script setup lang="ts">
import type { Inquisition } from "@/types";
import { PropType } from "vue";

const props = defineProps({
  item: {
    type: Object as PropType<Inquisition>,
    required: true,
  },
});
</script>

<template>
  <LabelValue label="Тема проверки" :value="props.item.theme" />
  <LabelValue label="Информация" :value="props.item.info" />
  <LabelValue label="Дата записи">
    {{ new Date(props.item.created).toLocaleDateString() }}
  </LabelValue>
</template>
