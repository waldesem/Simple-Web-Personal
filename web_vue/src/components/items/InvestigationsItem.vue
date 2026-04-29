<script setup lang="ts">
import { PropType } from "vue";
import { localStr } from "@/utils";
import type { Inquisition } from "@/types";

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
  <LabelValue label="Дата записи" :value="localStr(props.item.created)" />
</template>
