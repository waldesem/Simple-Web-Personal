<script setup lang="ts">
import { PropType } from "vue";
import type { Inquisition } from "@/types";
import { localStr } from "@/utils";

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
    {{ localStr(props.item.created) }}
  </LabelValue>
</template>
